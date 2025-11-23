---
creation date: 2024-03-25
Wiki Link:
  - https://adobe-my.sharepoint.com/:w:/r/personal/rmanor_adobe_com/_layouts/15/doc.aspx?sourcedoc=%7B37929b0e-c25f-404e-9397-789cce89b06a%7D&action=edit
---
# Needs 
- Examples of contextualization 
    - pre-recorded 
    - In - product (plugin)
    - What to demo
        - Photos, backgrounds, [[Icons]], design elements 
        - 3 - 5 min
            - 1 - 2 templates which show good results 
                - ENT - sales/advert/etc
                - Consumer - invites/insta/etc
        - Focus on results quality 
        - behavior to show 
            - Changing elements on the canvas, to display recs refresh 
                - Template 
                - Start from blank
            - Long form query for results refinement 
                - Photo only
                - A1 + USS
                    - _Vis [[Intent AI Home|CKG]] (stock tab)_  
                    - _If more than four tokens, use new stock endpoint with A1 embeddings*_ 
        - >4 token intent understanding
        - Stretch goal 
            - _All tab which displays all element types with topical ordering in editor based on text query*_

# Talk track 

Hi, I'm Ryan Manor, product manager for intent understanding here with a quick walk though of our contextual editor experience. 

To start let's imagine I'm a marketer for a (Coffee shop, photography store, fashion, XYZ) brand who's looking to promote a new (thing) with an Instagram post. I log into Express and start looking for the right template to use by making a search for ("asdf"). I scroll through the results, and see one that catches my eye, but I think they could make it perfect with a few edits, so I go to the editor. I add a few relevant details, and then decide to change a few of the elements around. In this scenario today, I would see a static set of icons and design assets for any given template, which may or may not be particularly useful.

But instead by using our contextual intent understanding we're able to tailor the element collections to the task at hand. Using info like my location, the time of year, the query I made to get here, and the contents of the template we can produce a much more relevant list of elements.

So instead of this static list they're greeted with a bespoke list of elements which relate to topic of the template. This saves the user from having to think about all the things they might possibly add, and saves them time searching millions of elements to find it. Now they can quickly get inspiration about where they might go with the template, and make those edits. Here you can see that because the template is about (XXXXX) I get collections like (XXXX), and (XXXXX). I can see these same topics in other element types as well. 

As I start to make changes to the template by adding or changing icons, text, and colors. The collections I get served change as well to follow suit with the evolving intent of my project. 

I quickly get the project to a place where I'm ready to export, and I schedule the post to go live on my instagram page. 

Now let's look at a more complex case, where an individual license user goes to make a project starting from a blank canvas and building it up themselves. 

In this case I'm a (person selling their car and making a social post, a person pinning a poster about a hiking/biking club on a community bulletin board, a hobby photographer selling family portrait shoots), so I'll be using some of my own content, and some Express elements. 

I being by choosing my aspect ratio and going to the editor. To start the recommendations don't have much context to go off of other than the location, time of year, and aspect ratio of the canvas, so they're a bit scattered. But with only an image and some text, we see the contextualization taking off and starting to turn up good results. Even with somewhat ambiguous text we can use the image as additional signal to clarify the intent and return good results. I quickly get inspired and start to add some of these element to my project. Each time I do, and each edit I make the more and more signal we have to create better results. This especially helps in scenarios where the user is starting from a blank canvas because of how lost or buried in choice users can feel when they don't have this kind of contextualization to rely on. 

This project is close, but i'd like to add one more image, something *extremely* specific. Normally this would mean that I might need to scroll through a lot of results on an image query for exactly what I want, or iterate on a query over and over to chip away at exactly what Im looking for. Luckily in my case, I don't have to do either. Here I can make use of a Stock index which has been enriched with Adobe One embeddings which create a much more semantically complete picture of a given asset. This means that longer, more specific queries can be handled, and the results ranked with much greater precision. I can now find *exactly* the kind of image I had in mind, and finish of this project. 

Here, we've looked at a few examples of how Contextual user indent understanding, and content understanding can come together and create much better user experience in Express. In the future we're looking to add aesthetic understanding to incorporate color harmonies and pallets, stylistic cues, and brand aware contextualization, and I look forward to sharing those changes as they're rolled out. Thank you. 




# Examples to use 
B2B
- Camera store 
	- urn:aaid:sc:VA6C2:d1acbd58-6d13-5990-b6ea-7f7f3954ef17
- Music Store 
	- urn:aaid:sc:VA6C2:245445bf-c67a-5132-bfea-b3425c6acd6b
- Climbing Gym 
	- urn:aaid:sc:VA6C2:ef1b03cf-9488-5c2f-97f3-f8db5e2e2ce9

Rando
