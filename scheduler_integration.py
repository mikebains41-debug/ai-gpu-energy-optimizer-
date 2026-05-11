#!/usr/bin/env python3
# GPU Telemetry Validation - Scheduler Integration
# Detects desync and triggers workload migration
# Phase 2: Turns detection into action

import argparse
import json
import subprocess
import sys

def evict_kubernetes_pod(pod_name, namespace, reason):
    """Evict a pod from Kubernetes when desync detected"""
    try:
        from kubernetes import client, config
        from kubernetes.client.rest import ApiException
        
        config.load_incluster_config()
        api = client.CoreV1Api()
        
        eviction = client.V1Eviction(
            metadata=client.V1ObjectMeta(name=pod_name, namespace=namespace),
            delete_options=client.V1DeleteOptions()
        )
        
        api.create_namespaced_pod_eviction(pod_name, namespace, eviction)
        print(f"✅ Evicted pod {pod_name} in namespace {namespace}")
        print(f"   Reason: {reason}")
        return True
        
    except ImportError:
        print("⚠️ Kubernetes Python client not installed")
        print("   Run: pip install kubernetes")
        return False
    except Exception as e:
        print(f"❌ Failed to evict pod: {e}")
        return False

def evict_runai_job(job_name, reason):
    """Evict a Run:ai job when desync detected"""
    try:
        cmd = f"runai delete job {job_name}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Deleted Run:ai job {job_name}")
            print(f"   Reason: {reason}")
            return True
        else:
            print(f"❌ Failed to delete job: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def send_slack_alert(webhook_url, pod_name, power_w, reported_util):
    """Send alert to Slack when desync detected"""
    try:
        import requests
        
        message = {
            "text": f"🚨 GPU Telemetry Desync Detected!\nPod: {pod_name}\nPower: {power_w}W\nReported Utilization: {reported_util}%\nAction: Workload will be migrated"
        }
        
        response = requests.post(webhook_url, json=message)
        if response.status_code == 200:
            print("✅ Slack alert sent")
            return True
    except:
        print("⚠️ Slack alert failed (webhook not configured)")
        return False

def main():
    parser = argparse.ArgumentParser(description='GPU Telemetry Scheduler Integration')
    parser.add_argument('--evict', action='store_true', help='Evict the workload')
    parser.add_argument('--pod-name', default='unknown', help='Kubernetes pod name')
    parser.add_argument('--namespace', default='default', help='Kubernetes namespace')
    parser.add_argument('--job-name', help='Run:ai job name')
    parser.add_argument('--reason', default='telemetry desync detected', help='Reason for eviction')
    parser.add_argument('--power', type=float, help='Power draw in watts')
    parser.add_argument('--util', type=int, help='Reported utilization percent')
    parser.add_argument('--slack-webhook', help='Slack webhook URL for alerts')
    
    args = parser.parse_args()
    
    if args.evict:
        print("=== GPU Telemetry: Scheduler Integration ===")
        
        if args.power and args.util:
            print(f"Detected: {args.power}W at {args.util}% utilization")
        
        if args.pod_name:
            evict_kubernetes_pod(args.pod_name, args.namespace, args.reason)
        
        if args.job_name:
            evict_runai_job(args.job_name, args.reason)
        
        if args.slack_webhook and args.power and args.util:
            send_slack_alert(args.slack_webhook, args.pod_name, args.power, args.util)
        
        print("\n✅ Action completed. Workload marked for migration.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
