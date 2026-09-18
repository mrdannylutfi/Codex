// src/billing/webhook.controller.ts
import { Controller, Post, Headers, Req, Res, BadRequestException } from '@nestjs/common';
import { Request, Response } from 'express';
import { PrismaService } from '../prisma.service';
import Stripe from 'stripe';

@Controller('webhooks/stripe')
export class StripeWebhookController {
  private stripe: Stripe;

  constructor(private prisma: PrismaService) {
    this.stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
      apiVersion: '2025-01-27.accredited',
    });
  }

  @Post()
  async handleWebhook(@Headers('stripe-signature') sig: string, @Req() req: Request, @Res() res: Response) {
    let event: Stripe.Event;

    try {
      // req.body must be the raw Buffer for signature verification to work
      event = this.stripe.webhooks.constructEvent(
        req.body,
        sig,
        process.env.STRIPE_WEBHOOK_SECRET
      );
    } catch (err: any) {
      throw new BadRequestException(`Webhook Error: ${err.message}`);
    }

    // Handle targeting subscription life-cycles
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session;
        const tenantId = session.metadata?.tenantId;

        if (tenantId) {
          await this.prisma.tenant.update({
            where: { id: tenantId },
            data: { plan: 'Enterprise', status: 'ACTIVE' },
          });
        }
        break;
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;
        // Retrieve tenant ID from metadata saved on the subscription or cross-referenced customer data
        const tenantId = subscription.metadata?.tenantId;

        if (tenantId) {
          await this.prisma.tenant.update({
            where: { id: tenantId },
            data: { plan: 'Free', status: 'SUSPENDED' },
          });
        }
        break;
      }
    }

    return res.status(200).json({ received: true });
  }
}
