#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/imgutils.h>

// Context container for our output stream
typedef struct OutputMuxer {
    AVFormatContext *fmt_ctx;
    AVCodecContext  *enc_ctx;
    AVStream        *stream;
} OutputMuxer;

// 1. Initialize libavformat and libavcodec for writing
int init_output_muxer(OutputMuxer *muxer, const char *filename, int width, int height, AVRational time_base) {
    int ret;
    const AVCodec *codec;

    // Allocate the output format context
    ret = avformat_alloc_output_context2(&muxer->fmt_ctx, NULL, NULL, filename);
    if (ret < 0) return ret;

    // Find a standard video encoder (e.g., H.264)
    codec = avcodec_find_encoder(AV_CODEC_ID_H264);
    if (!codec) return AVERROR(ENVOY);

    // Create a new video stream in the container
    muxer->stream = avformat_new_stream(muxer->fmt_ctx, NULL);
    if (!muxer->stream) return AVERROR(ENOMEM);

    // Allocate and configure the encoder context
    muxer->enc_ctx = avcodec_alloc_context3(codec);
    if (!muxer->enc_ctx) return AVERROR(ENOMEM);

    muxer->enc_ctx->width     = width;
    muxer->enc_ctx->height    = height;
    muxer->enc_ctx->pix_fmt   = AV_PIX_FMT_YUV420P; // Typically need to scale from sub2video's RGB32/PAL8
    muxer->enc_ctx->time_base = time_base;
    muxer->stream->time_base  = time_base;

    // Some formats want stream headers to be separate
    if (muxer->fmt_ctx->oformat->flags & AVFMT_GLOBALHEADER)
        muxer->enc_ctx->flags |= AV_CODEC_FLAG_GLOBAL_HEADER;

    // Open the encoder
    ret = avcodec_open2(muxer->enc_ctx, codec, NULL);
    if (ret < 0) return ret;

    // Copy encoder parameters to stream parameters
    ret = avcodec_parameters_from_context(muxer->stream->codecpar, muxer->enc_ctx);
    if (ret < 0) return ret;

    // Open the output file if required by the container
    if (!(muxer->fmt_ctx->oformat->flags & AVFMT_NOFILE)) {
        ret = avio_open(&muxer->fmt_ctx->pb, filename, AVIO_FLAG_WRITE);
        if (ret < 0) return ret;
    }

    // Write the stream header to the file
    ret = avformat_write_header(muxer->fmt_ctx, NULL);
    return ret;
}

// 2. Encode the AVFrame and write it using libavformat
int write_video_frame(OutputMuxer *muxer, AVFrame *frame, int64_t pts) {
    int ret;
    AVPacket *pkt = av_packet_alloc();
    if (!pkt) return AVERROR(ENOMEM);

    // Assign the presentation timestamp to the frame
    frame->pts = pts;

    // Send the frame to the encoder
    ret = avcodec_send_frame(muxer->enc_ctx, frame);
    if (ret < 0) {
        av_packet_free(&pkt);
        return ret;
    }

    // Read encoded packets from the encoder and write them to the container file
    while (ret >= 0) {
        ret = avcodec_receive_packet(muxer->enc_ctx, pkt);
        if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) {
            break;
        } else if (ret < 0) {
            av_packet_free(&pkt);
            return ret;
        }

        // Rescale timestamps from the encoder's time base to the stream's time base
        av_packet_rescale_ts(pkt, muxer->enc_ctx->time_base, muxer->stream->time_base);
        pkt->stream_index = muxer->stream->index;

        // Write the compressed packet to the media file
        ret = av_interleaved_write_frame(muxer->fmt_ctx, pkt);
        av_packet_unref(pkt);
        if (ret < 0) {
            av_packet_free(&pkt);
            return ret;
        }
    }

    av_packet_free(&pkt);
    return 0;
}

// 3. Close and clean up contexts
void close_output_muxer(OutputMuxer *muxer) {
    if (muxer->fmt_ctx) {
        av_write_trailer(muxer->fmt_ctx);
        if (!(muxer->fmt_ctx->oformat->flags & AVFMT_NOFILE)) {
            avio_closep(&muxer->fmt_ctx->pb);
        }
        avformat_free_context(muxer->fmt_ctx);
    }
    avcodec_free_context(&muxer->enc_ctx);
}
