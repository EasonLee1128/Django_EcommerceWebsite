# 整體架構:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/%E6%95%B4%E9%AB%94%E6%9E%B6%E6%A7%8B.jpg)

使用者連接到GCP的VMP的ORT號，GCP的VM運行兩個container。
- NGINX。
- Wsgi run django project。

NGINX透過Socket收到wsgi run django project的資訊，然後在指定VM的一個port號給NGINX使用，使用者連接VM的PORT號就能進入網站。

網頁流程:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/%E7%B6%B2%E7%AB%99%E6%B5%81%E7%A8%8B.jpg)
