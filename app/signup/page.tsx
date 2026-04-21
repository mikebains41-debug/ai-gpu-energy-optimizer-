/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { useState } from 'react';
import { Zap, CheckCircle, Loader2 } from 'lucide-react';

export default function SignupPage() {
  const [formData, setFormData] = useState({
    companyName: '',
    email: '',
    gpuTypes: '',
    monthlyEnergySpend: '',
    reason: ''
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/beta/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setSubmitted(true);
      } else {
        const data = await response.json();
        setError(data.error || 'Something went wrong');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
        <div className="max-w-md text-center">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-green-500/20 rounded-full">
              <CheckCircle className="h-12 w-12 text-green-400" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-100 mb-2">Application Submitted!</h1>
          <p className="text-gray-400 mb-6">
            Thank you for applying to the beta program. We'll review your application and send credentials within 24 hours.
          </p>
          <a href="/" className="text-blue-400 hover:text-blue-300">Return to Home</a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <Zap className="h-12 w-12 text-blue-500" />
          </div>
          <h1 className="text-3xl font-bold text-gray-100">Join the Beta Program</h1>
          <p className="text-gray-400 mt-2">Get 90 days free access to AI GPU Energy Optimizer</p>
        </div>

        <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6 md:p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Company / Lab Name *
              </label>
              <input
                type="text"
                required
                value={formData.companyName}
                onChange={(e) => setFormData({...formData, companyName: e.target.value})}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 focus:outline-none focus:border-blue-500"
                placeholder="e.g., AI Research Labs"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 focus:outline-none focus:border-blue-500"
                placeholder="you@company.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                GPU Types *
              </label>
              <input
                type="text"
                required
                value={formData.gpuTypes}
                onChange={(e) => setFormData({...formData, gpuTypes: e.target.value})}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 focus:outline-none focus:border-blue-500"
                placeholder="e.g., H100, A100, RTX 4090"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Monthly Energy Spend (USD) *
              </label>
              <input
                type="number"
                required
                value={formData.monthlyEnergySpend}
                onChange={(e) => setFormData({...formData, monthlyEnergySpend: e.target.value})}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 focus:outline-none focus:border-blue-500"
                placeholder="e.g., 5000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Why do you want to join the beta? *
              </label>
              <textarea
                required
                rows={4}
                value={formData.reason}
                onChange={(e) => setFormData({...formData, reason: e.target.value})}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 focus:outline-none focus:border-blue-500"
                placeholder="Tell us about your GPU cluster and goals..."
              />
            </div>

            {error && (
              <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              {loading && <Loader2 className="h-4 w-4 animate-spin" />}
              {loading ? 'Submitting...' : 'Apply for Beta Access'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
