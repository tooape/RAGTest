**Slide 1**
Hey I'm Ryan manor, I lead product for SDC's intent understanding tech, and [[Vic Chen|Vic]] and I will be talking a bit about an upcoming feature in express called [[Recommendations Home|contextual recommendations]]. 

**slide 2** 
Firstly, let's start with what contextualization is and why it's a problem to be solved. 

Our communicators have an overwhelming breadth of incredible content they might put in a project. But this itself presents a problem, because now they have to not only know what to add, but how to look for it. 
\
Here we see an example. I've got a template pulled up for a baby shower or a baby announcement or something, and you can see on the left hand side that the static collections of really beautiful images, but none of them are about babies. 

[[Recommendations Home|Contextual recs]] is a collab between a few different teams around Express aimed at creating a smooth and high quality asset discovery experience for any canvas, without making users think about how to structure a query, or what to query for. 

Over on the right you can see a little sneak peek at the contextualized categories for things like baby clothes and toys. We've shown these based on our understanding of the canvas, and the topics around that core creative intent, and then returned some relevant assets. 

**Slide 3** 
Let's break down how this flows a little bit. 

To start we take the canvas, the rendition, the inner text, and we send that over to a platform in SDC called "[[Intent AI Home|MINT]]", which I'll explain in just a minute. 
[[Intent AI Home|Mint]] first identifies the core creative intent of this canvas, here things like cafe, grand opening, and promos. But these topics aren't useful to the user at all. They know it's about these intents, they're looking right at it. So to make the recommendations, [[Intent AI Home|mint]] takes associations around these intents, so we might return things like barista, latte art, or open sign. These associations are what we then use to look for the relevant assets, and then display to the communicator as a recommendation. 

And that's really the broad strokes of what this is doing. But I think it helps to break down what [[Intent AI Home|MINT]] is a little bit. 

**Slide 4**
I promised [[Vic Chen|Vic]] I wouldn't give an AI lecture, so this won't get too nerdy.

Firstly, [[Intent AI Home|MINT]] or MINTs stands for Multi-Modal Intent service. It's biggest value is in taking the infinite range of possibilities that someone might come up with on an express canvas, and mapping that down to a finite set of canonicalized concepts. 

To do this we use two big pieces of tech... 

First we have the foundational AI model that takes in modalities like text or image and breaks them down in an interpretable way. And then [[Intent AI Home|CKG]], or creative [[Intent AI Home|knowledge graph]], which you can think of as a big web of concepts, and then links these all together. These concepts might be things like the subject matter of an image maybe skateboard, or surfer, or more abstract things like colors, or actions. 

As an example of this platform that yall might have seen already is in start from your content. When you upload an image you see these topic filters, which are the intents that [[Intent AI Home|MINT]] has extracted from the provided image. 

So now that we're all AI architects, what's the game plan? 

**Slide 5**
Ship it! 

We're rolling out our first test on photos, icons, design assets, and backgrounds next week. hopefully. 

you'll see them at the top of these respective tabs as a carousel of topics, each with a thumbnail asset called "ideas based on your file". 

This test is less about blowing the doors off the building with crazy lift in click through rates, than it is double checking ourselves. First in making sure that our recommendations are safe. We've tested our recs with all kinds of problematic data sets and collaborated with ethics to make sure we stay on the right side of things. But user's are whole different ball game. 

And second to test the technical design of how all this is hooked up. We need to make sure this will work at the kind of scale express sees before we go big. This is no good if it lights on fire and falls over in a day. 

This release is a pilot, and lays the foundation for everything we want to contextualize going forward. But what is it that we want to work up to doing? 

**Slide 6**
The roadmap going into next year can be thought of in two groups; 
1. powering more contextualization on more surfaces

Areas like the new all tab are a great candidate for this since users might expect to see a broad range of content there. 
Likewise there's been concepts floating around for this contextual command bar that would bring useful actions and assets to the user as the move around the canvas, this too would be a great place to bring our intent intelligence. 

2. improving the core tech 
Currently we can really only do graphic and textual inputs, we're looking to expand intent understanding into new modalities like audio and video. 
We'll also look to expand our understanding of how our concepts are applied in different cultural contexts. "Wedding" is a great example. There may be a term which translates to wedding in a million languages, but the culture around that will vary massively. how can we understand this and bring contextualization to more than US english speakers? 

And last, but most importantly Style understanding. 

Style and aesthetics are so obviously critical to creation. We believe there's so much to capture here, it's really it's own roadmap, and I could go for hours here. But first we're looking at ways to bring stylistic similarity into contextualization. Can we look at one asset of a cheeseburger, and show you the fries and the coke that look similar? After this we'll push into areas like aesthetic cohesion, and semantic style understanding to bring all of this intelligence to people in a communicable way. 

you can see here on the right some SUPER early work of us trying to group different assets by their look and feel rather than their topical subject matter. 

Also this is completely unrelated, but while making this deck I saw a groups feature, and I love these little stacks, they're so great with remove background. 


**Slide 7**
So all of this brings me to what my ask of yall is. 

We've done a credible job of establishing a base line, we've got relevant recommendations showing up for a wide range of products. But we don't have that special sauce. 

We know when to show you a pizza, some baby clothes, and some skateboards, but we don't know what makes the coolest looking skate baby pizza party invite. 

I'd love partnership and feedback from everyone here on how we can push [[Intent AI Home|MINT]] and our queries to that level of quality. How can we make contextualization feel hand picked? 

I use this image on the right a lot internally and I wanted to share this with yall. I use the metaphor of an art tutor, helping and guiding our users to make whatever it is they want to make better than they could have by themselves. 

And my team and I cannot accomplish this by ourselves. I'll share a playground later, and please give us the hard feedback, where dose this experience suck? Hopefully this time next year I'm back with yall showing off our great skater baby pizza results. 

**Demo**
So with that if I'm open to some questions, or if there's time i'd love to do what no PM in their right mind would do and try to run a live demo. 


