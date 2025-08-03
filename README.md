<img width="1256" height="720" alt="Architecture" src="https://github.com/user-attachments/assets/e3e322e2-72c8-4b43-8393-37fb49319eb8" />



# AWS Three-Tier Web Application Infrastructure 


---

## 1. Create VPC

- Create a new VPC with an appropriate CIDR block (e.g., 10.0.0.0/16).

---

## 2. Create 6 Subnets

| Tier         | Subnet Type | Number | 
|--------------|-------------|--------|
| Web Server   | Public      | 2      | 
| App Server   | Private     | 2      | 
| Database     | Private     | 2      |

---

## 3. Create Route Tables

- **Public Route Table:**  
  Attach Internet Gateway (IGW) and associate with 2 public subnets.

- **Private Route Tables:**  
  Create one private route table per private subnet.  
  Route internet-bound traffic through NAT Gateway in the respective availability zone for HA.

- **Database Route Table:**  
  By default, no NAT Gateway attached.  
  (Optionally add NAT Gateway for patching or updates.)

---

## 4. Create 5 Security Groups

| Security Group  | Allowed Traffic                                | Source                  |
|-----------------|------------------------------------------------|-------------------------|
| WebServer-SG    | SSH (22), HTTP (80), HTTPS (443)               | Anywhere (0.0.0.0/0)    |
| AppServer-SG    | Port 5000, SSH, HTTP(80), HTTPS(443)           | WebServer-SG            |
| DB-SG           | MySQL (3306)                                   | AppServer-SG            |
| Additional-SG1  | (Optional) Custom rules                        | Define as needed        |
| Additional-SG2  | (Optional) Custom rules                        | Define as needed        |

---

## 5. Setup Route 53 Hosted Zone

- Create a Hosted Zone in Route 53 for your domain.
- Update your domain registrar's name servers to the Route 53 NS records.

---

## 6. Validate ACM Certificate

- Request an SSL certificate for your domain via AWS Certificate Manager (ACM).
- Validate domain ownership by creating the required CNAME record in Route 53.

---

## 7. Create RDS MySQL Instance

- Create a DB Subnet Group with at least 2 private subnets.
- Launch MySQL RDS instance within private subnet, associated with DB-SG.

---

## 8. Launch Web Server EC2

- Deploy EC2 instances in public subnet.
- Attach WebServer-SG to instance.

---

## 9. Launch App Server EC2

- Deploy EC2 instances in private subnet.
- Attach AppServer-SG to instance.

---

## 10. Connect to App Server


vi mumbai_r.pem

chmod 400 mumbai_r.pem

ssh -i mumbai_r.pem ubuntu@<App_Server_Private_IP>

---

## 11. Setup Database Client on App Server

sudo apt update

sudo apt install mysql-client -y

mysql -h <RDS_endpoint> -P 3306 -u admin -p

---

## 12. Setup App Server Environment

sudo apt update

sudo apt install python3 python3-pip python3-venv -y

python3 -m venv venv

source venv/bin/activate

pip install flask flask-mysql-connector flask-cors

nohup python3 app.py > output.log 2>&1 &

ps -ef | grep app.py

cat output.log 

curl http://localhost:5000/login

---

## 13. Setup Web Server (Apache)

sudo apt update

sudo apt install apache2 -y

sudo systemctl start apache2

cd /var/www/html/

sudo touch index.html script.js styles.css

---

## 14. Create Application Load Balancer (ALB)

Create **Backend Target Group** for App Server EC2 with:

   . Port: 5000
   
   . Health Check Path: /login
   
Create **Backend Load Balancer** in the public subnet with:

   . Listener Port: 80
   
   . Attach the Target Group
   
Create **Frontend Target Group** for Web Server EC2 with:

   . Port: 80
   
   . Health Check Path: /
   
Create **Frontend Load Balancer** in the public subnet with:

   . Listener Port: 80
   
   . Attach the Target Group

---

## 15. Configure Route 53 to Load Balancer

Create an A record with alias pointing to the Frontend Load Balancer.

---

## 16. Attach ACM Certificate to Load Balancer








