# davidtrubridge.com inventory (measured 2026-10-26, isolated headless Chromium 1440x900 and 390x844)

Method: Python Playwright, sequential page loads, computed styles + CSS/JS grep of the theme's own app.css/app.js (one fetch each). Screenshots in this folder: 01-home, 02-nav-open (desktop menu + Shop panel), 03-collection-pendants, 04-product-coral (full), 04b-product-top (viewport), 05-studio, 07-commissions, 08-stockists, 09-inspiration, 10-bcorp, 11-m-home, 12-m-product, 13-m-menu-open (14 files). `/pages/projects` is an empty 175px shell (just an H1 "Projects"); real projects page = `/blogs/commissions`. No separate "about" beyond `/pages/studio`; `/pages/about` and `/pages/contact` exist in the menu but were not visited (time-box). Note: full-page PNGs are 1484px wide at 1440 viewport (something causes ~44px horizontal overflow, scrollWidth 1484 on home); do not replicate.
Confidence tags: [M] measured from DOM/CSS, [I] inferred.

## 1. Tech signals
| Item | Finding |
|---|---|
| Platform | Shopify (`powered-by: Shopify`, `/cdn/shop/t/12/`), custom Tailwind-style theme by General Studios (footer credit "Site by General Studios"). Utility classes (`py-30`, `md:gap-y-50`, `aspect-[380/370]`) [M] |
| Animation libs | None of GSAP/ScrollTrigger/Lenis/Locomotive/AOS (0 hits in app.js, no globals) [M]. Everything is CSS transitions + a few keyframes (`fade-in` .3s, `fade-up` translateY(75px)->0) |
| Carousel | Swiper (class `swiper--featured-content-trio`, pagination dots clickable, slidesPerView 1 base) in product page testimonials/featured content [M]; home shows none |
| Smooth scroll | None; `scroll-behavior:auto` [M] |
| Video | Home hero + studio hero + product hero = full-viewport muted looping `<video>` (autoplay, loop, muted, playsInline). Home hero source is HLS `.m3u8` (Shopify-hosted, 852px wide stream); product page has 4 videos (lit/unlit variants x ?) with MP4 1080p; IntersectionObserver in app.js plays/pauses videos at `rootMargin 200px` [M]. Vimeo link for "Watch the film" |
| Video player | Plyr (`--plyr-color-main:#424941`) [M] |
| Fonts | Sanomat (display serif, self-hosted woff2 "Light" file declared wt 500) + FT System (grotesque sans, `FTSystem-BlankRegular` + Italic woff2). Only 2 families, 1 weight each [M] |
| Third party | Klaviyo, Facebook pixel, GTM/gtag, Shopify Shop-pay, Regios automatic discounts, Google Maps (stockists), a reviews app |
| Transitions | Native CSS View Transitions used for page changes (`--view-transition-old/new-main-content`: .125s ease-in-out fade) [M] |

## 2. Global design tokens (all [M])
| Token | Value |
|---|---|
| Page bg | `#F6F6F6`; many sections `bg-white` (#FFF); cream `#F6F2ED`; footer `#424941` |
| Text | `#1A1A1A`; forest ink `#232E28` (headings in cream/white sections); on dark `#FFF` / cream `#F1EDE3` |
| Accent | Almost none: black buttons; forest green button `#3F5349` / text `#F1EDE3`; promo band brown `#3A2620`; star gold `#9C7539`; pill hairline `#D9D0BE` |
| Hero h1 | Sanomat 74px/74px wt500 ls 1.48px, white, bottom-left at x30 |
| Page h1 | 68px/74.8px ls1.36px (Commissions, product); collection h1 53px/58.3px ls1.06px; Where to Buy h1 ~74px |
| h2 | Sanomat 34-44px, lh 1.15-1.25, ls .02em; sub-sections 28px/30.8 |
| Body | FT System 14px/16.8px; paragraphs 14-16px, ls -0.01em, very tight lh ~1.2 |
| Nav | FT System 14px wt400, no transform, no letter-spacing |
| Buttons | 14px, padding 10px 40px, 1px border, radius 0; `.btn--primary` black fill white text -> hover black/white (`.2s cubic-bezier(.4,0,.2,1)`); `.btn--green` (#3F5349/#F1EDE3, 600, ls .28px, 14x28, radius 4px); `.btn--outline` 1px #232E28 radius 4px, hover fills; `.btn--link` underline, hover opacity .7 |
| Eyebrow | 12px UPPERCASE ls 1.44px lh 14.4px ("IN REAL HOMES"); pill tag 11px upper ls .44 on rgba(255,255,255,.92) radius 999 pad 5x10 |
| Accordion titles | FT System 30px wt500 ls -1px lh30px, pad 15/0/20 (product FAQ, 500px column) |
| Container | Full-bleed with 20px gutters (30px hero/promo); promo inner 1200px (x120); b-corp text block 580px wide |
| Section padding | 100px top/bottom on every `.section-padding` [M]; hero pad 30px |
| Grid gap | Product grid gap-x 30px, gap-y 50px; 3 columns (446.7px each at 1440); card image aspect 380/370 on cream |
| Radii | Mostly 0; green/outline buttons 4px; filter pills 999px; review cards 4px |
| Shadows | None measured |

## 3. Nav (all [M] unless noted)
- **Announcement bar**: 57px dark olive strip above header (`notification-bar`), centred 14px white text "Free signed copy of David's book... Ends Mon 26 Oct", dismiss X at right (x1395). Scrolls away (not sticky).
- **Header** (65px, `.global-header#main-nav`): logo left (x20, 130x47, `)david trubridge` stacked wordmark), two plain text links at x220 and x369 ("Shop Kitset Lighting", "Shop Seconds Sale"), right cluster: flag + "$NZD" currency button (x1268), "Cart" text button (x1347), 25px two-line burger (x1395). No search icon, no cart icon (text "Cart").
- **Transparent over hero** on `/` and `/pages/studio` (white text/logo, bg transparent); on all other pages bg #F6F6F6 with dark text. Scroll behaviour: hides when scrolling down, reappears on scroll up as `position:fixed; top:0; background:#FFF` with class `nav-sticky--show` (no shadow). Header bg transition .2s.
- **Menu = left slide-in drawer, click-to-open (burger), NOT hover.** 480px white panel (`mega-menu__col`, max-width 33.33vw at wide) slides from translateX(-100%) in 1s `cubic-bezier(.41,.38,.14,1)`; page dims with #1A1A1A backdrop at .4 opacity (.4s). Title "Menu", close X at x445. Items (~30px, ~36px row pitch, inferred size from screenshot): Shop, Design Support, Where to buy (direct link), Our Work, Our Responsibility, About Us; footer of drawer shows phone +64 6 650 0204 and "Showroom Directions" (Google Maps).
- **Second-level panel**: clicking a top-level item opens a second 480px cream (#F6F2ED) panel beside it (x480-960), with staggered fade/translate-up (items start translateY(30px) opacity 0, 1s ease, 1s delay).
  - Shop: image cards Pendants / Other Products / Seconds (420x161 rows, hairline top border, label top-left 14px, product cutout right) + black "View All" button 440x39.
  - Design Support: Digital Brochure, Inspiration Gallery, Render Contact, Trade Contact.
  - Our Work: Commission Projects, Writings by David, David's Web Series, + "View All" (/pages/projects).
  - Our Responsibility: B Corp Profile, Find Out More (sustainability).
  - About Us: Meet the Maker, Studio, Contact, + "View All" (/pages/about).
- **Mobile 390**: same header (logo x20, "$NZD" x233, "Cart" x305, burger x345), drawer becomes full-width 390x844 white, items 15px (measured) stacked: Shop, Design Support, Where to buy, Our Work, Our Responsibility, About Us, Showroom Directions. Mobile h1 40px/40px, h2 28px/32px; product h1 31px. No horizontal overflow (scrollWidth 390).

## 4. Pages (1440 wide; y = absolute page y, h = height)
### 4.1 Home `/` (total 6479; 01-home.png)
| # | Section | y / h | Layout, content, image treatment |
|---|---|---|---|
| 0 | Announcement bar | 0 / 57 | see nav |
| 1 | Hero `section--hero` | 57 / 900 (100vh) | Full-bleed autoplay muted looping HLS video of the studio building; header transparent on top; H1 "Studio & Workshop" (74px white, bottom-left x30, 2 lines) and white "Watch the film" button (300x37, black text, pad 10/40, links to Vimeo). Video scrolls away normally (measured: no parallax, moves 1:1 with scroll) |
| 2 | Promo banner `promo-banner--live` | 997 / 262 | Brown #3A2620 band, inner 1200px; left: product-image thumb (book) in white rounded frame; date pill "23-26 October" (1px white border, 4px radius, 14px ls .56 pad 4x12), H2 36px/41px white "A free signed copy of The Other Way with orders over $299", 14px sub, underlined "Promotion details" |
| 3 | "Where most people start:" `recommended-products` | 1299 / 1277 | pad 100px. H2 (Sanomat 40px/50px, 584px wide, left, x234) beside a 2x2 grid of product cards (each 505x524 at x380/x915, gap 30/30) |
| 4 | Values band `b-corp-banner` | 2576 / 593 | Cream with 5% opacity leaf-pattern background image; 3 centred columns (Seed System Kitsets / Proudly NZ Made / B Corp score of 102.8): badge icon, Sanomat 28-40px title, 14px copy, text links wt600 with arrow, "View more on our B Corp profile" + "More on our sustainability commitment" |
| 5 | Commissions split `commissions-split-panel` | 3169 / 1075 | 2 columns: left 650px-wide tall (~640px) image/looping video (detail of woven amber form, bleeds to left edge x0..~700); right x784: H2 34px "Some of Our Best Work", 14px copy 541px wide, buttons "Enquire" (green fill 108x47, r4) + "See commission projects" (outline 227x47, r4) |
| 6 | In real homes `in-their-homes` | 4244 / 867 | UPPERCASE eyebrow "IN REAL HOMES" (12px ls1.44) + H2 36px "Real spaces, real customers."; 3 tall (403px-wide inner) portrait photo cards in 1400px row (x20.., ~30px gap), each with product tag top and cream 15px/23px testimonial overlaid bottom-left on dark gradient |
| 7 | Store reviews `store-reviews` | 5111 / 571 | H2 44px/48px "In good company!..." (720px wide left); gold stars + "4.9 out of 5 from 11 store reviews" 15px; 3 white review cards (456x203, pad 24, radius 4): gold stars (#9C7539 ls 2px), Sanomat 19px review headline, 14px body, reviewer name |
| 8 | Footer | 5682 / 798 | see 6 |

### 4.2 Collection `/collections/pendants` (4075; 03-collection-pendants.png)
Announcement (57) + header (65) + promo banner (262, y153) + grid section (y455, h2822). Header row: H1 "Lighting" Sanomat 53px left x20; right: "Sort by: Featured" select (137x19) + 2 grid-density icons (3-col/2-col toggle, [I]). Grid: 15 products, 3 cols x 5 rows; card = `a.card--product`, image box `aspect 380/370` bg cream #F6F2ED (447x447 at 1440, `object-fit` cover-ish lifestyle cutout on beige photographic backdrop with soft shadow), below: name left 14px, "From $389.00" right-aligned grey 14px; row pitch 467+50. No add-to-cart on card. Hover [M from CSS]: card bg transparent->#FFF over .5s, image gets 5% black overlay (`#0000000d`) over .3s; optional "badge" top-right (12px uppercase white r10).

### 4.3 Product `/products/coral` (10865; 04-product-coral.png, 04b-product-top.png)
| # | Section | y / h | Notes |
|---|---|---|---|
| 1 | Product hero `section--product` | 57 / 900 | Full-viewport looping muted video background (dark room, lamp lit; 4 videos = variants/colours), header transparent-white; H1 "Coral" 68px white left-bottom (y537); 4-line 16px intro copy 380px wide; "View Light Mode" toggle (half-moon icon, 14px) switches lit/unlit video; bottom bar (hairline top border) with variant thumb row 150x150 (colour swatch), size/colour selects (3 cells divided by vertical hairlines at x370, x765), price `$389.00` and white "Add to Cart" button 263x39 (pad 10/40, black text, 1px black border) at x1158 |
| 2 | "For Every Space, A Masterpiece" `text-with-detail` | 957 / 688 | Centred H2 + 3 gallery captions (e.g. "Coral 600mm Bamboo @casasolstad") carousel/row of customer photos |
| 3 | Product story | 1645 / 328 | 2 col: product thumb left, paragraph right |
| 4 | Accordions `faqs` | 1972 / 1031 | 500px-wide column x500: 30px/500 ls -1px titles ("Seed System Kitsets", "Easy Assembly", "Inspired by Nature", "Available in Colours", "Regenerating Waterways", "Cleaning the Coastlines") with +/- icons, hairline separators; illustration image alongside |
| 5 | Reviews | 3003 / 1245 | "Customer reviews" 4.6/5, star-distribution bars, sort pills, review list |
| 6 | "Form by day, mood by night." `light-in-your-space` | 4248 / 835 | Full-bleed render of a room with the lamp, H2 40px white left; size selector list (400mm/600mm/... 21px buttons) swaps rendered image (30 images preloaded) [M: 30 imgs in section], "Day/Night" toggle |
| 7 | Technical information `product-information` | 5083 / 2775 | H2 "Technical Information" centred; left sticky-looking tab list (Dimensions, Packaging, Finishes, Materials, Free Shipping, What You Receive, Lamp Required, Installation & Components, Warranty, Care Instructions, Awards, Assembly Videos, Downloads); right 920px column at x500 with line-drawing diagrams + spec tables (key/value rows 14px) |
| 8 | Testimonial `testimonials` | 7858 / 607 | Giant Sanomat pull-quote (~48-60px) + Swiper pagination dots |
| 9 | Half-half `half-half` | 8465 / 1035 | Two big image tiles w/ overlaid heading + "Learn More"/"View Now" button: "How to choose a light" and "Get Inspiration" |
| 10 | Related `related-products` | 9500 / 567 | "Grow Range" 3 cards (same card as collection) |
Mobile product (12-m-product.png, 14260 tall): hero h1 31px; cards go 350px full width.

### 4.4 Studio / About `/pages/studio` (9556; 05-studio.png)
Hero video 900 (H1 "Design Studio" 74px + 16px/19px paragraph 380px wide + "View Commissions" button) -> `reveal-section` (957/900): 3 tabs "1 Artistry / 2 Ideation / 3 Design" (30px, inactive opacity .5, click toggles cross-fading panels .3s) over a full-width landscape photo + side caption; `text-with-detail` statement (1857/572, large 2-paragraph copy); Team (2429/2214): H2 "Our Team", filter list (Leadership/Office/Workshop/Design & Marketing) left, 3-col grid of 300x375 portrait photos on teal bg with name + role below (10 people); Image CTA "David Trubridge HQ" (4642/1035) full-bleed building photo with big heading + paragraph overlay; Awards (5677/3080): year-row table, year left col, 2 columns (project | award) at x480, hairline row separators, pad 15/0/0.
### 4.5 Commissions `/blogs/commissions` (4559; 07-commissions.png)
H1 68px; full-width (1400) featured project video/image (~640px tall) with one-line description left (22-28px) + black "View Project" button right; "All Commissions 13" label with hairline above and "Filters" column on right; **masonry-ish 3-col grid of mixed aspect ratios** (portrait, landscape, tall), captions Sanomat-like 18px below each, pagination "1 2 v".
### 4.6 Where to Buy `/pages/stockists` (2011; 08-stockists.png)
H1 74px left; right column: "Search Our Stockists" with country/region selects as 30px underlined dropdowns (hairline bottom, chevron); big Google Map (915x830, x497..1412) with greyscale styling, stockist list (left, 20 images) beside it.
### 4.7 Inspiration Gallery `/pages/inspiration-gallery` (4065; 09-inspiration.png)
Cream (#E?; ~#EFE8DA [I]) hero: gold eyebrow "INSPIRATION GALLERY", H2 44px "See it living.", 14px copy, buttons "Browse the gallery" (green) + "Send us your space" (outline); sticky-feeling white filter bar of pill chips (13px, pad 8x16, radius 999, hairline #D9D0BE; active = #232E28 fill/#F1EDE3 text) + "18 spaces" count right; 3-col grid of landscape/portrait room photos, each with white 92% uppercase 11px tag top-left and 2-line caption (title 14px + grey sub-caption 12px); dark forest CTA band (#232E28) "Have a David Trubridge light living in your space?" 28px cream + gold "Submit your space" button.
### 4.8 NZ Made & B Corp `/pages/nz-made-bcorp` (4460; 10-bcorp.png)
Video hero 640px ("Watch the full video") -> content split (701): eyebrow "WHY IT'S MADE HERE" + H2 "Proudly NZ Made" + copy + image; B Corp block (959) "VERIFIED IMPACT / Certified B Corporation" with stat counters (`bcb-stat-number`, labels .85 opacity); LCA/EPD split with 3 sub-headings (848); closing CTA band (458) with 1 sentence heading.
### Not found / not visited
No standalone "lookbook"; closest = Inspiration Gallery + Commissions. `/pages/projects` empty. `/pages/contact`, `/pages/about`, `/pages/meet-the-maker`, FAQs not captured.

## 5. Animations / interactions
| Where | Effect | Source | Confidence |
|---|---|---|---|
| Drawer menu | 1s slide-in `cubic-bezier(.41,.38,.14,1)`, second panel items stagger fade-up (30px, 1s delay) | CSS vars + computed transitions | [M] |
| Header | Hides scrolling down, returns white-fixed on scroll up; transparent-white over video hero pages | class toggles `nav-sticky`, `nav-sticky--show` | [M] |
| Product card hover | Card bg -> white (.5s), image +5% black overlay (.3s) | app.css | [M] from CSS; not visually recorded |
| Buttons | color/bg .2s `cubic-bezier(.4,0,.2,1)`; link buttons opacity .7 | CSS | [M] |
| Hero videos | Autoplay muted loop, played/paused by IntersectionObserver (200px margin) | app.js | [M] |
| Scroll reveals | None found: below-fold sections load at opacity 1, transform none (measured on /, collection, studio); only keyframe `fade-up` exists, applied to menu items/buttons | probe | [M] |
| Parallax | None (hero moved exactly 300px for 300px scroll) | probe | [M] |
| Image zoom / cursor effects | None found | CSS grep | [I] |
| Studio tabs | click cross-fade .3s, inactive trigger opacity .5 | probe | [M] |
| Page transitions | CSS View Transitions .125s fade | CSS vars | [M] |
| Product light/dark | "View Light Mode" toggle swaps hero video; size picker swaps room renders | DOM | [M structure], effect [I] |

## 6. Footer (`#shopify-section-footer`, 798px, bg #424941, pad 30px 0, white 14px text)
Two-zone layout: left 700px = white logo top, bottom: "Permanent Sponsor of the Maraetotara Tree Trust" (icon + 14px grey) and Certified B Corporation badge; right x740 (680px): 3 link columns at x740 / x967 / x1193 (225px pitch) with 12-14px muted headers "Shop" (Lighting, Other Products, Where to Buy), "Learn" (FAQ's, About, Commissions, Product Care Guide, Contact, Sign Up To Our Newsletter), "Social" (Instagram, Facebook, Pinterest, YouTube). Below, stacked blocks separated by 1px white hairlines: phone + underlined email; "Sign up to our newsletter" with underline-only email input (680x23, pad 0 0 5, 14px) and "Sign up ->" text button (12px); address "2 Groome Place, Whakatu, Hastings, Hawkes Bay". Bottom row: (c) line left, Terms & Conditions / Privacy Policy at x740/x875, "Site by General Studios" right x1270.

## 7. Borrowable for a lighting concept store (ranked)
1. **Full-viewport video hero with transparent header** - 100vh muted/loop/playsinline video (HLS or MP4 1080p), H1 Serif 74px/74px ls .02em white bottom-left at x30/y(100vh-190), one white button 300x37 pad 10/40 black text. Header transparent+white text until scroll, then white on scroll-up. Pause off-screen with IntersectionObserver (rootMargin 200px).
2. **Hide-on-scroll-down / show-on-scroll-up header**: 65px, `position:fixed; top:0; background:#fff` on reveal, bg transition .2s, no shadow.
3. **Left slide-in drawer menu with a second cream panel** - 480px white column + 480px #F6F2ED column, backdrop #1A1A1A@.4, 1s `cubic-bezier(.41,.38,.14,1)` in / `cubic-bezier(.82,.22,.65,.87)` out; top-level items ~30px Sans; sub-panel rows 161px tall with hairline top border, label top-left, cut-out product right; staggered fade-up of rows.
4. **Two-font system**: Sanomat-like high-contrast serif for headings (wt 500 faux, ls +0.02em, lh ~1.0-1.15 on display sizes) + neutral grotesque 14px/16.8px body with -0.01em tracking. Palette: #F6F6F6 / #1A1A1A / forest #232E28 / footer #424941 / cream #F6F2ED / one gold #9C7539. Almost no accent colour; photography carries it.
5. **Quiet product grid**: 3 cols, gap-x 30 / gap-y 50, 20px page gutters, square-ish image (aspect 380/370) on cream backdrop, name left + "From $x" grey right at 14px, no CTA; hover = bg->white + 5% black wash (.3-.5s). Header row: serif H1 53px left, "Sort by" right, 3/2-col density toggle.
6. **Product page = cinematic hero + purchase bar**: 100vh looping video of the lamp lit in a dark room, serif H1 68px, 380px intro, "View Light Mode" lit/unlit toggle, bottom bar with hairline border containing variant selects (cells split by vertical hairlines), price, and white 263x39 Add to Cart.
7. **"Light in your space" size/render picker**: full-bleed room render + H2 40px; list of size buttons 21px (white text, underline on active) that swap pre-rendered room images (30 images); a lighting-store-specific proof-of-scale pattern.
8. **Technical Information block**: H2 centred, left tab/anchor list of spec categories, right 920px column of line-drawing diagrams + 2-col key/value tables (14px, hairlines). Pair with 30px/500 ls -1px accordions (500px column) for FAQs/story.
9. **Inspiration gallery with pill filters**: gold 11px eyebrow, 44px serif H2, filter chips 13px pad 8x16 radius 999 hairline #D9D0BE (active #232E28/#F1EDE3), count right, 3-col photo grid with white-92% uppercase 11px tag (pad 5x10, r999) top-left + title/sub-caption below, closing forest-green CTA band "Send us your space" (28px cream serif + gold button).
10. **Promo band as editorial**: #3A2620 brown 262px band, 1200px inner, product thumb in white frame, date pill (1px border r4 14px ls .56 pad 4x12) + 36px serif headline - sale messaging without a pop-up.
11. **Values/trust band**: cream bg with 5%-opacity botanical pattern, 3 centred columns (certification icon + 28-40px serif + 14px copy + wt600 text link with arrow), sits directly below the product grid.
12. **Review cards + giant pull-quote**: white cards 456x203 r4 pad 24, gold stars ls 2px, 19px serif headline; on product page a single 48-60px serif testimonial with Swiper dots.
13. **Awards/credentials table**: year left, 2-col rows at x480, 15px top pad, hairline separators (reuse for stockists/press).
14. **Footer**: forest-grey #424941, big white logo left, 3 link cols at 225px pitch right, underline-only newsletter input, hairline-separated contact blocks, sponsor + certification badges bottom-left.
