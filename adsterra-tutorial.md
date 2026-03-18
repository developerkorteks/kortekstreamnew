Ad Units and Code Snippets
Selecting the Right Ad Unit
Selecting the Right Ad Unit
Discover how to choose the ad unit for your website that will monetize 100% of your traffic


Written by Ana M
Updated over 6 months ago
Table of contents
💡 An Ad Unit is a specific advertising format you can place on your website. It does not define the category of ads your audience will get, but rather the format of the advertisement. We can divide Ad Units into two broad categories: rich media ads and static ads. Popunder, Social Bar and Native Banners usually bring the best results and highest profits.

 

Rich Media Ads
Rich media ad may include video, audio, or other elements that encourage your visitors to interact with the content. While display ads sell with static images, rich media ads offer more ways to engage an audience, and increase your CTR.

 

 

Social Bar

Social Bar is one of the most engaging and interactive ad formats; it can look like in-page push, chat bubbles, custom banners, icons, quizzes, etc. You may find some examples here.

 

Great for:

websites with well-built UX;

iOS users monetization;

bypassing Ad Block.

Pricing models: 75% for CPA, 20% for CPM and 5% for CPC.

Fine-tuning your ads: reach out to us if you would like to change the position (like upper-left or bottom-right corner) or how often you want your visitors to see the ad.

 

 

Popunder

Popunder is full-page adverting, which looks like a landing/an offer page, appearing in a tab behind the main browser window.

 

Great for: websites with an audience that doesn't like to be distracted from the content, who is likely to focus attention on one thing per time.

Pricing models: 50/50 CPM/CPA.

Fine-tuning your ads: we can help you set up the frequency of your Popunder, as well as whether it opens on any click or only for certain elements.

 

 

Smartlink
 


Smartlink is a URL that takes users who click on it to an offer page. The best offer page is selected by our system for each user depending on their GEO, OS, device and other targeting.

 

Pricing models: 50/50 CPM/CPA.

Great for: publishers who don't own a website, monetization of social traffic, websites with limited space for ad placement.

 

 

 

 

Static Ads
Static ads include Banners of various sizes and Native Banners. Both are non-intrusive and can be placed on any web page, but are prone to banner blindness.

 

Native Banners

Native Banner is a block of banners in which content and headlines blend with the website's content. They are responsive, and their performance relies highly on its strategically picked location.

 

Great for: websites and blogs with featured content.

Pricing models: a mixture of CPM/CPA/CPC ad campaigns

Fine-tuning your ads: you can select the layout, font size and colour on the Websites page. Reach out to us if you'd like to customize what it looks like on mobile devices or add custom CSS.

 

 

Display Banners

A static image with or without text that you can insert at a chosen place on your website. Note that it is not responsive and will not automatically adjust its size for mobile devices, however we provide Banner sizes that fit smaller screens well. Here you can also find a guide on how to display different Banners on different devices.

 

Pricing models: CPA

 

We offer the following Banner sizes: 160x300, 160x600, 300x250, 320х50, 728x90, 468x60. 

160 x 300 — would look great in the sidebar or footer in-between other interface elements.


160 x 600 — Wide Skyscraper — a little longer than the previous one, but still fits the sidebar as a standalone ad.

300 x 250 — Medium Rectangle — usually placed near the top of a webpage, and works best when placed before the fold.

 
728 x 90 — Leaderboard — perfect for headers and footers, and is often placed above the main content of a page.

320 х 50 — Mobile Leaderboard — opt for this one instead of the leaderboard for mobile devices.


468 x 60 — usually referred to as 'Banner Ad' — often appears at the top of a webpage.

 
We recommend placing a Banner of any size in high-traffic locations on web pages, including the front, bottom, or the side of a webpage. 

You may see the demo version of all ad formats here.

Let's continue by placing ads on a site!


Adding Ads to a Static HTML Site
Learn how to install Adsterra's advertising codes onto your static pages


Written by Ana M
Updated over 6 months ago
Table of contents
💡 We'll walk you through the process of adding Adsterra ads to a very simple static HTML page, however the process is roughly the same for more complex websites as well. Our codes are JavaScript based and work on almost any website. However, if you prefer WordPress, Elementor, Blogger or a php-based site, please refer to the relevant guides. The code snippets are always available on the Websites page — in this article you'll find our step-by-step guide to getting the scripts.

 

Popunder
Add the code snippet right before the closing </head> tag:

 


❗ Note that using several Popunder codes on the same page may lead to conflict of the codes. If you want to increase the number of ads, just reach out to us to set customized frequency settings.

 

 

Social Bar
Social Bar script is placed right above the closing </body> tag:

 


❗ Note that changing the position of the code snippet does not place the ads elsewhere — please get in touch if you want to change the location of the ads. Also bear in mind that using several Social Bar codes on the same page does not increase the number of ads. If you want to change it, just contact us to set customized frequency settings.

 

 

Smartlink
Using your Smartlink in a Text:

To add a Smartlink to any text, use the standard HTML <a> tag for hyperlinks:

<a href="your smartlink URL">link text</a>
 You can also add it to any image:

<a href="your smartlink URL"> <img src="https://adsterra.com/_nuxt/img/logo_extended.fddf2fa.svg" alt="Adsterra"> </a>
 Or even add it to a button:

<button onclick="window.location.href='your smartlink URL';"> Click Here </button>
 


 

Native Banners
Native Banner script can be placed anywhere in the page body:

 


The ad will inherit the style of the webpage by default; on the Websites page you can tweak the layout, as well as the size and colour of the font.

 


❗ Note that using the same Native banner code more than once per page may lead to conflict of the codes. You may ask for up to 2 additional Native Banner codes by contacting our Support team.

 

 

Static Banners
For Static Banner, just place the code snippet anywhere in the page body, but keep in mind that horizontal banners look better at the top of the page, and vertical ones are mainly used in the sidebar. Rectangle ads can be placed almost anywhere.

 


💡 Note that we do not provide ads.txt files, as our advertisers do not require them.

If you still need it, you can contact us to request the required details and create the file on your own. We'll be glad to share the needed data with you!




Installing Adsterra Ads to WordPress
Learn how to install Adsterra's advertising codes on your Wordpress blogs and sites


Written by Ana M
Updated over 10 months ago
Table of contents
💡 WordPress allows you to add our codes to all pages at once, a specific page or even into any one post. We'll be using WordPress 5.7.1 in this guide, so please be mindful that there may be minor differences if your version is different. You can always look up adding custom HTML in your WordPress documentation.

 

Adding Ads to Every Page
Installing our ads to every page of your WordPress website usually requires editing the theme. There are two ways to do that:

 

Editing the Source Code
It works best for Social Bar and Popunder codes, however you can add almost any Ad Unit. To access the theme:

Click 'Appearance' and select 'Theme Editor' from the left-hand menu;

Find the theme element you'd like to add the code snippet to under the 'Theme Files' on the right;

Click the element name (for example, Theme Header or Theme Footer) to see its source code;

Where you paste the code snippet depends on the Ad Unit:

To add a Popunder, paste the code snippet right before the closing </head> tag (usually available in the 'Theme Header' file);

To add a Social Bar, paste the code snippet right before the closing </body> tag (usually available in the 'Theme Footer' file);

Banners and Native Banners can be placed anywhere in the page body, but make sure it fits in well.

Click 'Update file' below to save the changes.

 


Placing the Code Snippet via Widgets
Widgets are more convenient when working with Native Banners and Banners, as they are a bit more visual. 'Custom HTML' is the only widget you'll need to install any Adsterra Ad Unit, however you can also use 'Text' widget if your WordPress version is below 4.8.1 and does not support 'Custom HTML'

Click 'Appearance' and select 'Widgets';

Select on the 'Custom HTML' widget;

Check the theme element and click 'Add Widget'; the widget will open in the element section;

Paste the code snippet into the widget and click 'Save'.

Bear in mind that you may need to double-check if the code snippets you added are still available whenever you switch your WordPress theme.

 


 

Placing an Ad on a Single Page
If you want to have an ad on a specific page only, you can add the 'Custom HTML' widget to this page only. This will work for any Ad Unit as well.

Select 'Pages' from the left-hand menu;

Mouse over the page you'd like to modify and select 'Edit';

Click ➕ and select 'Custom HTML'

Insert the code snippet into the text box;

Click 'Update' in the upper right corner.


Having added the code, you can click 'Preview' to check if the ad has been installed correctly.

 

 

Adding an Ad to a Post
Native Banners and horizontal Banners would look the best within a post, right after the title or between two paragraphs. We'll use the 'Custom HTML' widget for this as well.

Navigate to 'Posts' from the left-hand menu;

Find your post in the list, hover over its title and select 'Edit';

Click ➕ in the upper left corner and scroll down to Widgets

Paste the script from the Websites page into the widget;

Click 'Update' in the upper right corner.


When adding the ads, make sure your scripts don't conflict: if you have a Social Bar or Popunder in your theme, adding the same ad unit to a specific page or post may prevent both codes from working.

 

 

💡 Note that we do not provide ads.txt files, as our advertisers do not require them.

If you still need it, you can contact us to request the required details and create the file on your own. We'll be glad to share the needed data with you!




Adding Adsterra ads to a php-based website

Written by Victoria V
Updated over 3 months ago
Table of contents
Intro
💡 PHP is a server-side language you can use to build your website. When someone opens your website, their browser sends a request to your server, where PHP code generates HTML and sends it back to the browser.

In practice, PHP websites are structured into multiple files to keep the code organized and reusable. A typical setup includes at least three basic files:

index.php – the main page, which assembles the different parts of your site.

header.php – contains the <head> section, navigation, and scripts that should load at the top.

footer.php – contains closing tags, footer content, and scripts that should load at the bottom.

The main page (index.php) usually includes the header and footer files using PHP’s include or require statements. This modular approach makes it easy to manage your site, update repeated elements, and insert Adsterra ads consistently across pages.

Ad placement recommendations
Popunder should always be placed before </head>.

Social Bar should always be placed before </body>.

Banner ads and Native ads can be placed flexibly:

Above or below the navigation in the header

Inside the article content

In a sidebar (<aside>)

Place no more than four banner ads per page to avoid banner blindness and thus hindered traffic performance. Always ensure ads are positioned thoughtfully to maintain user experience.

Testing Your PHP Website with Adsterra Ads
 

Before publishing, it’s important to verify that your ads appear correctly. You can test your site online using free hosting or locally using the PHP built-in server. Both methods allow you to preview your site and confirm ad functionality.

 

A. Online Test with Free Hosting (e.g., InfinityFree)
 

1. Register on a free hosting platform and create a website with a free domain.

2. Upload your three basic PHP files: index.php, header.php, footer.php into the hosting file manager:


3. Insert your Adsterra code snippets: place banners and native ads in the page body, Popunder before </head>, and Social Bar script before </body> :


4. Open your site using the provided domain in a browser to verify correct ad display.

Tip: For beginners, keeping all three files in the root folder is sufficient. For larger projects, you can organize files into subfolders.

B. Local Testing Using PHP Built-in Server
Local testing allows you to preview your site without uploading it online:

1. Create a project folder on your computer (e.g., PHP_site).

2. Create three PHP files: index.php, header.php, footer.php and include your Adsterra ad code:



3. Open Command Prompt and navigate to your project folder:

cd "C:\Users\User\Desktop\PHP_site"
4. Install PHP via Scoop (if not already installed):

scoop install php
5. Start the PHP built-in server:

php -S localhost:8000

6. Open your browser and go to http://localhost:8000 to see your site and ads in action.


Any changes to your files are reflected immediately when you refresh the page.

Placement and Styling Tips
 

Proper styling ensures that ads look natural and engage users effectively:

Use <aside> for sidebar placement, <header> for top banners, and <footer> for bottom scripts.

Center ads with CSS when needed:

.ad-container {
    text-align: center;
    margin: auto;
}
Maintain a maximum of four ads per page to prevent banner blindness.

Test multiple placements locally or online to determine which positions perform best.

💡 Note that we do not provide ads.txt files, as our advertisers do not require them.

If you still need it, you can contact us to request the required details and create the file on your own. We'll be glad to share the needed data with you!




Search for articles...
All Collections
Ad Units and Code Snippets
Using Adsterra Ads with Cloudflare
Using Adsterra Ads with Cloudflare
Learn how to prevent RocketLoader from adding extra text to Adsterra's advertising code


Written by Ana M
Updated over 2 months ago
💡 Cloudflare has a feature called "RocketLoader" which causes changes to our javascript code and therefore our script works in the wrong way or does not work at all, affecting your impressions and revenue.

 

Here is an example of how RocketLoader changes our script.

Our script:

<script type='text/javascript' src='//effectivegatecpm.com/82/6d/f3/826df33e1880e1ab086c8406879dc14e.js'></script>
Our script after it was affected by RocketLoader:

<script type="text/rocketscript" data-rocketsrc='//effectivegatecpm.com/82/6d/f3/826df33e1880e1ab086c8406879dc14e.js'></script>
 

In order to prevent RocketLoader from adding extra text to our code, you should add data-cfasync="false" attribute into our code just before the type attribute:

<script data-cfasync="false" type='text/javascript' src='//effectivegatecpm.com/82/6d/f3/826df33e1880e1ab086c8406879dc14e.js'></script>



Displaying Different Banners on Mobile and Desktop
Learn how to use Adsterra's Banners for mobile and desktop traffic


Written by Ana M
Updated over a year ago
Table of contents
💡 Even though our Banners are not responsive, you can easily show and hide different sizes depending on the device. This simple CSS trick will show you how.


Installation
All you need to do is just to add this code exactly where you need the Banners to be showing:

<style type="text/css">
  .mobileShow {display: none;}

  /* Smartphone Portrait and Landscape */
  @media only screen
    and (min-device-width : 320px)
    and (max-device-width : 480px){ 
      .mobileShow {display: inline;}
  }
  .mobileHide { display: inline; }

  /* Smartphone Portrait and Landscape */
  @media only screen
    and (min-device-width : 320px)
    and (max-device-width : 480px){
     .mobileHide { display: none;}
  }
</style>

<div class="mobileShow"> Your code snippet for mobile </div>

<div class="mobileHide"> Code snippet for desktop only </div>
❗️Don't forget to insert Banner codes from your personal area instead of 'Your code snippet for mobile' and 'Code snippet for desktop only'.

 

You can use any method of installation: directly to HTML (however, not into the <head> section), by adding widgets / gadgets, custom HTML element, etc.

 

The most optimal combination is 728x90 and 320x50 Banners, however, you can choose any you like.

 

 

Checking if It Works
Chrome Dev Tools allows you to check how your website looks on different devices.

Open your website, right click anywhere on the page and select 'Inspect'; Chrome Dev Tools panel will open.

Click Toggle Device Toolbar in the upper-right corner of the panel.

Select the mobile device from the drop-down.



