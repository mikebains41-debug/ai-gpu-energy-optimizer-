// PROPRIETARY AND CONFIDENTIAL
// Copyright (c) 2026 Mike Bains. All Rights Reserved.
// Contact: Mikebains41@gmail.com
// Unauthorized use prohibited.

import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendCredentialsEmail(
  email: string, 
  companyName: string, 
  clusterId: string, 
  apiKey: string
) {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }
        .credentials { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3b82f6; }
        .code { font-family: monospace; background: #e5e7eb; padding: 10px; border-radius: 5px; font-size: 14px; word-break: break-all; }
        .button { display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin-top: 20px; }
        .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>🎉 Welcome to AI GPU Energy Optimizer!</h1>
          <p>Your Beta Access Credentials</p>
        </div>
        <div class="content">
          <p>Hello <strong>${companyName}</strong>,</p>
          <p>Congratulations! You've been accepted into the AI GPU Energy Optimizer beta program.</p>
          
          <div class="credentials">
            <h3>🔐 Your Credentials</h3>
            <p><strong>Cluster ID:</strong><br><code class="code">${clusterId}</code></p>
            <p><strong>API Key:</strong><br><code class="code">${apiKey}</code></p>
            <p><strong>Expires:</strong> ${new Date(Date.now() + 90*24*60*60*1000).toLocaleDateString()}</p>
          </div>
          
          <h3>🚀 Installation Instructions</h3>
          <p>Run this command on any Linux/macOS GPU server:</p>
          <pre class="code">curl -sSL https://raw.githubusercontent.com/mikebains41-debug/ai-gpu-energy-optimizer-/main/ai-engine/install.sh | bash</pre>
          
          <p>When prompted, enter your credentials above.</p>
          
          <a href="https://ai-gpu-energy-optimizer.vercel.app/dashboard" class="button">View Your Dashboard →</a>
          
          <p style="margin-top: 20px; font-size: 14px; color: #6b7280;">
            Need help? Reply to this email or contact <a href="mailto:Mikebains41@gmail.com">Mikebains41@gmail.com</a>
          </p>
        </div>
        <div class="footer">
          <p>© 2026 AI GPU Energy Optimizer. All rights reserved.</p>
        </div>
      </div>
    </body>
    </html>
  `;

  try {
    await resend.emails.send({
      from: 'onboarding@resend.dev',
      to: email,
      subject: 'Your AI GPU Optimizer Beta Credentials',
      html: html,
    });
    console.log('Email sent to:', email);
    return true;
  } catch (error) {
    console.error('Email error:', error);
    return false;
  }
}
