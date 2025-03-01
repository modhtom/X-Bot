from Helpers import TweetClient as client , Email as email
import traceback
import random

def tweet_images():
    global image_index
    bot=client.TwitterBot()
    links=["https://i.pinimg.com/736x/c7/27/78/c727787916dac04f5ca765b20f0a4c93.jpg",
           "https://i.pinimg.com/564x/6b/46/f6/6b46f6594717c5691e9e8cc29918d067.jpg",
           "https://i.pinimg.com/564x/00/bd/6e/00bd6e21d75812bdc1a51e0990617bc6.jpg",
           "https://i.pinimg.com/736x/31/56/d0/3156d0853633217fb1f6fc6b7648a6f6.jpg",
           "https://i.pinimg.com/736x/bf/83/2f/bf832fe2b3627f6dfb1f3aa2e9f15526.jpg",
           "https://i.pinimg.com/564x/91/5b/aa/915baae542f19d0568f11272204af775.jpg",
           "https://i.pinimg.com/564x/09/c4/4b/09c44b818497e3ab5a1f92c5946843f0.jpg",
           "https://i.pinimg.com/564x/c8/cf/99/c8cf99688be7c2c1f1d33fe5165818c5.jpg",
           "https://i.pinimg.com/564x/ab/18/ca/ab18cabd1d540fa37c9fd05f2b96b89a.jpg",
           "https://i.pinimg.com/564x/a6/24/1d/a6241d4244df5e721200d7fe43921927.jpg",
           "https://i.pinimg.com/564x/d4/70/16/d47016f920d62c24dce19dc4c3aaa203.jpg",
           "https://i.pinimg.com/564x/fb/58/eb/fb58eb2141c13ce738ff68bb56013269.jpg",
           "https://i.pinimg.com/736x/6f/aa/6f/6faa6f3680b7f03807fe5bb9c03116ec.jpg",
           "https://i.pinimg.com/564x/34/69/52/34695258a8f05ed9113bc29b198cd6d5.jpg",
           "https://i.pinimg.com/736x/10/2b/90/102b90a7476bb8cace3a6ae723de59c7.jpg"
           ] 
    try:
       img = random.choice(links)
       bot.i_tweet(img)
    except Exception as e:
       error_message = (
            f"An error occurred while tweeting tweet_images.\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
       print(error_message)
       email.send(error_message)