**First of all:** Don't take this text seriously!

# Caching to not waste

To not waste what? Resources, hardware, and most importantly, time!

## A long-winded story behind it all

If you're like me and hate losing time (or have weak hardware that ever freezes or almost explodes when you try to run a giant workflow), this custom node is for you.

This node was built to cache all repetitive things that can be reused in a workflow: images, masks, controlnet images, and texts.

But what is a cache?

If you don't know, a cache it's a temporary kind of memory/file/storage used to access things used with high frequency.

E.g.: Imagine you want to find milk inside your refrigerator. So you open the refrigerator door, look for the milk, and close it. Do you notice that opening, looking for, and closing the refrigerator door costs time and effort?

If you take a picture of the inside of the fridge, and hang it on the door, every time you need to see what is inside the refrigerator, you can look at the picture and save all the time and effort to open and close the door.

On the ComfyUI, it's the same thing.

I have a workflow that used to... hum.. well... Let's say that is for removing things from a picture and putting other things in the same place 😇

In this Workflow, I have about two or three image resizes, twenty segment anything and mask creators, three different kinds of image prompts, three controlnet image generators like openpose, depth, and canny, and a lot of related nodes to work with it all. Result: the generation time to inpaint one image of 512px to 768px it's about 40 seconds. When the workflow finishes, most of the time it stops in the middle with a big alert: "OUT OF MEMORY!"

Ok, I understand the problem. In the end, I have been trying to load the checkpoint (SD 1.5), at least three Loras, the models of ground dino, segment anything, openpose, depth pose, controlnets, image to prompt, and so many other models and packages that my hardware can't stand it.

But, if I can execute most parts of these things only once and after that skip all these repetitive steps? I will save a lot of memory, processing, work, effort, and most importantly, time!

As I didn't find a custom node that do it for me, I must obligated to make mine.

## How does this work?

You just connect the main picture to the caching nodes and the Workflow's reuse part result. Internally, the node will generate a unique checksum hash of this main picture and save the "part result" of this execution in a file. Then every time you run this workflow, with this main picture, the caching nodes will only return this file, em vez de executing all of the nodes that make this service to you again, and again, and again...

Enough to resize images every run. Enough to generate an openpose, depthmap, canny, segment things, generate a lot of masks, and combine them with all other things every single time you run your workflow.

After that, my workflow (take a look at its size below) decreased from 40 seconds to 13 seconds! Sixty-seven fucking percent less than time! And better, if you're like me, and have a lot of pre-ready prompts to inpaint this same image, if you run all in one shot, the time decreases to about 8 seconds by generation! Eighty fucking percent of time savings!

<center>
<img src="https://raw.githubusercontent.com/alastor-666-1933/caching_to_not_waste/refs/heads/master/examples/from_40_seconds_to_10_seconds.png" width="100%"/>
</center>


Take a look at the workflow below. The first time it runs, it resizes the image, generates an openpose image, generates a text from MiaoshouAI Tagger, segments, and combines 12 masks. On my machine, this execution takes 20 seconds. But after the first run, with all these steps cached, it takes only 0.3 seconds to finish!

<center>
<img src="https://raw.githubusercontent.com/alastor-666-1933/caching_to_not_waste/refs/heads/master/examples/test.png" width="100%"/>
</center>

This is magic! The magic of saving 19.7 seconds on every run of inpaint you would perform with this image!

Ok, I explained what this node is for and the story behind its creation. Now let's go to the brief documentation part.

All caching nodes have the same inputs:
original_image: the main image will be linked with the cache
executor: the entire segment of an execution will result in an image, mask, controlnet image, or text, and should be cached (and never executed again)
identification: one input to select or type the identification of this cache (this identification must be unique)
force_recreate: a flag to force the node to ignore the actual cache and create a new one (don't forget to turn it off after recreating)

For some reason, the input "executor" of the caching text node was not like a connector, so you need to convert it into a connector to use. Just drag some output-type text to it, and it's done.

The cache images will be placed on /Comfyui/output/caching_to_not_waste. When you want, just delete the folder content.

Important: Every caching node must have a unique "identification"; if not, the cache will be replaced!

Important 2: The cache it's shared with all workflows, as long as you use the same "original_image" and "identification"

To see example workflows, just download it here: https://github.com/alastor-666-1933/caching_to_not_waste/tree/master/examples

## Examples

### Caching Text

<center>
<img src="https://raw.githubusercontent.com/alastor-666-1933/caching_to_not_waste/refs/heads/master/examples/caching_text.png" width="100%"/>
</center>

### Caching Prompt/Conditioning

<center>
<img src="https://raw.githubusercontent.com/alastor-666-1933/caching_to_not_waste/refs/heads/master/examples/caching_conditioning.png" width="100%"/>
</center>

### Caching Masks

<center>
<img src="https://raw.githubusercontent.com/alastor-666-1933/caching_to_not_waste/refs/heads/master/examples/caching_mask.png" width="100%"/>
</center>

### Caching Images

<center>
<img src="https://raw.githubusercontent.com/alastor-666-1933/caching_to_not_waste/refs/heads/master/examples/caching_image.png" width="100%"/>
</center>

### Caching Controlnets

<center>
<img src="https://raw.githubusercontent.com/alastor-666-1933/caching_to_not_waste/refs/heads/master/examples/caching_controlnet.png" width="100%"/>
</center>

### All Caching working together

<center>
<img src="https://raw.githubusercontent.com/alastor-666-1933/caching_to_not_waste/refs/heads/master/examples/caching_all.png" width="100%"/>
</center>

Now, go be happy! \😈/