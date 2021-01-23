1.  Users

    > Register

        -> Login
        -> Logout
        -> Profile
        -> Image
        -> Text
        -> Follow Button

    > Feed

        -> Users feed only
        -> User + who user follow

2.  Tweets

    > Creating

        -> Text ==> Media storage server of sometype.
        -> Image

    > Delete
    > Retweet

        -> Readonly serializer
        -> Create only serializer

    > Liking

3.  Following and Followers

## extra

1. blank = True > Django
2. null = True > database
3. Ajax call in Django

   $.ajax({
   type: "POST",
   url: url,
   data: dataRetrived,
   dataType: 'json',
   success: function(response){
   const tweetEl = document.getElementById("tweets") // how to get html element
   loadTweets(tweetEl)
   $('#content').val('')
   },
   error: function(){
   console.log("data is NOK")
   }

   })

4. Obj creation of Mnay2many field

obj.likes.add()
obj.likes.remove()
obj.likes.set() # requires qs
TweetLikeUser.objects.create(user=user, tweet=id)
