import { NextRequest, NextResponse } from 'next/server';
import { sendCredentialsEmail } from '@/lib/email';

// In-memory storage (use a database in production)
const betaApplications: any[] = [];

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { companyName, email, gpuTypes, monthlyEnergySpend, reason } = body;

    // Validate
    if (!companyName || !email || !gpuTypes || !monthlyEnergySpend || !reason) {
      return NextResponse.json({ error: 'All fields are required' }, { status: 400 });
    }

    // Generate credentials
    const clusterId = `${companyName.toLowerCase().replace(/\s/g, '-')}-${Math.random().toString(36).slice(2, 10)}`;
    const apiKey = `gpu_opt_${Math.random().toString(36) + Math.random().toString(36)}`;
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 90);

    // Save application
    const application = {
      id: Math.random().toString(36).slice(2),
      companyName,
      email,
      gpuTypes,
      monthlyEnergySpend: parseInt(monthlyEnergySpend),
      reason,
      clusterId,
      apiKey,
      expiresAt: expiresAt.toISOString(),
      status: 'pending',
      createdAt: new Date().toISOString()
    };
    betaApplications.push(application);

    // Send email with credentials
    await sendCredentialsEmail(email, companyName, clusterId, apiKey);

    return NextResponse.json({ success: true, message: 'Application submitted' });
  } catch (error) {
    console.error('Signup error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json(betaApplications);
}
