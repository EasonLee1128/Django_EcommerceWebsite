# 整體架構:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/%E6%95%B4%E9%AB%94%E6%9E%B6%E6%A7%8B.jpg)

GCP的VM使用DOCKER運行兩個container。
- NGINX。
- Wsgi run django project。

NGINX和wsgi run django project的資訊透過Socket傳遞，然後在指定VM的一個port號給NGINX使用，使用者連接VM的PORT號就能進入網站。
# 網頁架構:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/%E7%B6%B2%E7%AB%99%E6%B5%81%E7%A8%8B.jpg)

網站首頁: 列出網站商品，並將商品以6個進行分頁，可以使用按鈕(add to cart)將商品加入購物車，也可以透過(view)進入個別商品內頁。

左上角會顯示當前使用者名稱，若非本網站用戶會顯示AnonymousUser，依照是否為使用者透過JS調整HTML顯示前端
- 網站用戶: 顯示Register跟Log in。
- 非網站用戶: 顯示Log out 跟 Profile，Profile內頁有可以修改帳戶資訊。

右上角顯示目前購物數量，並可以進入購物車，
點入購物車後，可以在調整訂單，若OK可以進入結帳，
結帳串接Pypal的API，結完帳後即訂單成立。
