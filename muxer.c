int main() {
    Mp4BurnMuxer muxer = {0};
    
    // Explicitly target your specified Windows target directory
    // Ensure you use double backslashes for standard Windows paths in C string literals
    const char *output_destination = "C:\\Users\\mrdan\\OneDrive\\Pictures\\Cini\\burned_output.mp4";
    
    int video_width = 1920;
    int video_height = 1080;
    AVRational frame_rate = {30, 1}; // 30 FPS

    int ret = init_mp4_muxer(&muxer, output_destination, video_width, video_height, frame_rate);
    if (ret < 0) {
        printf("Failed to initialize MP4 container context.\n");
        return ret;
    }

    /* Processing Loop Logic Context:
    while (get_next_raw_video_frame(&video_frame)) {
        AVFrame *sub_frame = ifp->sub2video.frame; 
        
        // Burn subtitles directly onto the frame 
        blend_subtitle_to_video(&muxer, video_frame, sub_frame);
        
        // Write out package
        encode_and_write(&muxer, video_frame, calculated_pts);
    }
    */

    // Flush encoder context caches 
    encode_and_write(&muxer, NULL, 0);

    close_mp4_muxer(&muxer);
    return 0;
}
