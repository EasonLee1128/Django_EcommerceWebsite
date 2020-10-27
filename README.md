# 操作影片:
[![Watch the video](https://free.com.tw/blog/wp-content/uploads/2016/10/%E5%B5%8C%E5%85%A5-YouTube-%E5%BD%B1%E7%89%87%E7%82%BA%E9%9F%B3%E6%A8%82%E6%92%AD%E6%94%BE%E5%99%A8%E6%95%99%E5%AD%B8%EF%BC%8C%E5%83%85%E4%BF%9D%E7%95%99%E9%9F%B3%E6%A8%82%E9%BB%9E%E6%93%8A%E8%87%AA%E5%8B%95%E6%92%AD%E6%94%BEyoutube-audio-player-icon.png)](https://youtu.be/f7hU8jfO5kM)
# 整體架構:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/%E6%95%B4%E9%AB%94%E6%9E%B6%E6%A7%8B.jpg)

Google Cloud Platform的虛擬機使用Docker運行兩個Container。
- Nginx
- Wsgi run django project

Nginx與Wsgi透過Socket溝通，然後將指定一個Port給Nginx使用，提供使用者進入網站。

# 網頁架構:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/%E7%B6%B2%E7%AB%99%E6%B5%81%E7%A8%8B.jpg)

網站首頁: 

列出網站商品，並將商品以6個進行分頁，可以使用按鈕(add to cart)將商品加入購物車，也可以透過(view)進入個別商品內頁。

左上角會顯示當前使用者名稱，若非本網站用戶會顯示AnonymousUser，依照是否為使用者透過JS調整HTML顯示前端
- 網站用戶: 顯示Log out 跟 Profile，Profile內頁有可以修改帳戶資訊。
- 非網站用戶: 顯示Register跟Log in。

右上角顯示目前購物數量，並可以進入購物車，
點入購物車後，可以在調整訂單，若OK可以進入結帳，結帳串接Pypal的API，結完帳後即訂單成立。

# Cart.js邏輯:

使用addEventListener，當前端click按鈕(add to cart)，有兩個Function依照是否為網站用戶選擇使用。 
- add cookie item: 若不是網站用戶，使用cookie紀錄用戶的購物車明細傳入後端，之後用reload更新網頁。
- update user order: 用fetch將前端的資訊用json傳入後端更新訂單，之後用reload更新網頁。

# 實際頁面:
- 網站首頁:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/%E7%B6%B2%E7%AB%99%E9%A6%96%E9%A0%81.jpg)
- 帳戶資訊:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/profile.jpg)
- 註冊頁面:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/register.jpg)
- 登入頁面:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/LOGIN.jpg)
- 商品內頁:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/view.jpg)
- 購物車:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/cart.jpg)
- 結帳:
![image](https://github.com/Joyang0419/Django_EcommerceWebsite/blob/master/image/checkout.jpg)
