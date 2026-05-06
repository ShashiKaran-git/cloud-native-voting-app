# EKS Learning Lab

A cloud-native learning project built using AWS EKS, Kubernetes, Helm, Terraform, Docker, Redis, and PostgreSQL.

## 🚀 What I Built

- Dockerized microservices application
- Kubernetes deployments and services
- Helm-based Kubernetes packaging
- Terraform infrastructure provisioning for AWS EKS
- Redis + PostgreSQL integration
- AWS LoadBalancer exposure

## 🛠️ Tech Stack

- AWS EKS
- Terraform
- Kubernetes
- Helm
- Docker
- Python Flask
- Redis
- PostgreSQL (RDS)

## 📚 Key Learnings

- Kubernetes pod scheduling
- Helm templating and values management
- Terraform infrastructure provisioning
- Debugging CrashLoopBackOff and Pending pods
- AWS EKS networking and LoadBalancer behavior
- Resource optimization on low-cost clusters

## ⚠️ Challenges Faced

This project involved multiple real-world Kubernetes and AWS troubleshooting scenarios. 

While deploying on `t3.micro/t3.small` nodes, I faced:
- pod scheduling limits (`Too many pods`)
- memory pressure issues
- LoadBalancer debugging
- Kubernetes resource constraint handling

This project helped me better understand real-world Kubernetes troubleshooting and cloud infrastructure limitations.

## 🔮 Future Improvements

- GitHub Actions CI/CD
- Prometheus + Grafana monitoring
- Horizontal Pod Autoscaling
- ArgoCD GitOps workflow
