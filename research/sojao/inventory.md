# sojao.shop whole-site inventory (observed 2026-10-26, headless Chromium 1440x900 and 390x844)

Method: isolated Python-Playwright Chromium (probe scripts p*.py here). Computed styles read from live DOM. "MEASURED" = read from DOM/CSS/animation state; "INFERRED" = from screenshots/structure. Popups (Klaviyo, Hotjar, Yotpo) stripped before screenshots. The site rate-limits bare `curl` of the homepage (`local_rate_limited`) but loads fine in a browser UA. Screenshots: 01-10 desktop full-page, 11/12 mobile full-page (home/product), 13 mobile menu.

## 1. Tech signals
| Item | Finding |
|---|---|
| Platform | **Shopify**, theme **Impact 3.1.1** (Maestrooo) customised by agency Jumpstart (`[Main] Sojao x Jumpstart`; custom sections `jsc_section_set_builder`, `jsc-image-w-text`, `jsc-sticky-prod-gallery-desktop`). Web components (`mega-menu-disclosure`, `slideshow-carousel`, `product-gallery`, `video-media`) |
| JS libs | jQuery 3.6 + Flickity (only the Set Builder tab carousel: no wrap, no dots/arrows, draggable, cellAlign left, contained). No GSAP, Lenis, Swiper, AOS. No smooth-scroll lib (MEASURED: `window` has only Flickity+jQuery) |
| Animation | CSS only: keyframe `translateFull` marquees, opacity fades, `reveal-on-scroll` attribute on the slideshow. Theme has `reveal-on-scroll` helper but no visible card stagger (INFERRED from screenshots; not exhaustively confirmed) |
| Fonts | Heading **Poynter Oldstyle Display Regular** (typenetwork webfont) - overrides theme var `Cormorant`; body **Instrument Sans** 400/700 (self-hosted woff2 on Shopify CDN); nav links **Neuzeit Office** (loaded, sans); legacy unused: Proxima Nova, Sailec, Montserrat, Lora, Open Sans |
| Video | Hero slideshow = 3 slides, each with separate desktop (aspect 1.775) and mobile (aspect 0.667) MP4 (`<video-media>`, loop, muted, playsinline, preload metadata, no native autoplay attr - JS plays). About page has 1 video section ("From seed to sheets"). No GIFs |
| 3rd party | Klaviyo (popup/forms), Yotpo (reviews + loyalty), Hotjar, MS Clarity, GTM/GA/Meta pixel, Elevar, Instafeed (nfcube), RevenueHunt (sheets quiz), HulkApps form builder, easylocation |
| Mobile | No horizontal overflow at 390 (scrollWidth 390) on home and product |

## 2. Global design tokens (MEASURED; also tokens.json)
| Token | Value |
|---|---|
| Ink text | `#0A273D` rgb(10,39,61) |
| Accent / headings / primary button | `#29378C` rgb(41,55,140) (deep ultramarine navy) |
| Rust accent | `#BA5028` (announcement text, mega-menu column titles, NEW & sale badges, Journal hero bg, footer "Sleep Easy Club", star ratings) |
| Cream | `#F2F0EB` (footer, Set Builder band, icon-USP strip); page bg `#FFF`; product image tile ~`#E5E5E5` |
| Border | `rgba(10,39,61,.12)` |
| Radii | **0px on everything** (buttons, cards, inputs, badges are rect or circle); swatches/pills 9999px |
| Container | max 1800px; gutter 48px at 1440 (content x 48-1392); theme grid gutter 20px; product list gap 48px row / 24px col |
| Section padding | sections are flush (0 padding on wrapper); internal rhythm ~48-96px; section H2 sits ~72px under previous block |
| H (serif) | Poynter 500, ls -0.02em, lh 1.1: hero 48/52.8, section H2 40/44 (-0.8px), product H1 48/52.8, collection H1 **80/80 (-1.6px)**, scrolling-feature title 60/66, pledge band 48 |
| Body | Instrument Sans 16/25.6 400, ink |
| Eyebrow | 12px / 500 / ls 2px / uppercase / navy |
| Button | 16px / 700 / ls 1px / uppercase, pad 17.2x40 (hero, 60px high) or 14x32 (54px), bg navy, white text, no radius; hover bg -> navy@0.85 (.15s ease-in-out). Secondary: white bg, navy text, 1px navy border (e.g. "TAKE QUIZ ->"). Small "+ ADD": 12/700, pad 8x20, bg ink@10% |
| Nav link | Neuzeit Office 16/400 navy, hover = 1px underline `transform .25s ease-out` (`hover-underline-animation`) |
| Product card | image square 316x316 (cover/contain), title 16/400 centred (bold-ish in carousels = 700), price 16 "From $x" grey-ink, round colour swatches 26px with 1px #D3D3D3 border + "+N" overflow chip |
| Badges | circle 50px: NEW (rust bg, white 11px bold), BACK IN STOCK (yellow circle, black), SALE/SAVE 13% (navy rect), SOLD OUT (dark circle) |

## 3. Announcement bar + Nav
- **Announcement** (42px, bg `#F2F0EB`-ish cream, rust 16px text with rust bullet separators): continuous **marquee** (`translateFull` 39.9s linear infinite) of 3 messages: "NEW IN - Organic Heavyweight Tees" / "Free express shipping to APAC ... above SGD 450*" / "Same Day In-Store Pick Up Available" / "Free Delivery In Singapore...". Scrolls away (not sticky: `sticky-announcement-bar-enabled 0`).
- **Header** (74px): logo **SOJAO** wordmark left (serif, ~120px wide, x48), 7 centred links, search / account / cart icon trio right (22px icons at x1278/1324/1370). Logo + nav are **white-on-hero (transparent) at scroll 0**, then header becomes white bg with navy text once scrolled (sticky from ~scroll 300+: position sticky top 0, h 74). Sticky enabled. MEASURED at scroll 0: header bg transparent, logo white; at 1200: logo navy, sticky.
- Links (in order): **Bedding v**, **Bath v**, **Life & Lounge v**, Home & Living v, Last Call!, Gift Cards, Journal (4 with menus, 3 plain; Last Call/Gift Cards/Journal are plain links).
- **Mega-menus: HOVER-triggered** (`<details is="mega-menu-disclosure" trigger="hover">`; summary also has data-url to its collection page so click navigates). Panel full-width white, starts y116, page behind dims via `box-shadow 0 0 0 9999px rgba(0,0,0,.4)`; hovered link gets underline. Column titles rust 24px (serif-ish, theme submenu-title 24px), links navy/ink 16px, descriptions 16px/1.2 grey.
  - **Bedding** (tallest, ~736px): col1 "New In" (Butter, Barley & Frost); col2 "All Bedding" (Fitted Sheets, Duvet Covers, Quilts & Blankets, Pillow Cases, Bolster Cases, Body Pillow Cases, Flat Sheets, Baby Cot Sheets, Shop All); col3 "Shop By Fabric" (Classic Sateen - "Buttery-smooth and super soft organic cotton bedding"; Crisp Percale - "Extra breathable and lightweight"; Last Call!); second row "Bedding Sets" (Build Your Set, Duvet/Quilt/Fitted Sheet/Duvet/Quilt/Flat Sheet Sets); right: **2 promo image tiles** (220x147-ish) with white bold uppercase overlay labels ("SHOP NEW SHEET COLOURS", "NEWLY RESTOCKED - STONE").
  - **Bath** (~310px): list (Bath Towels, Hand Towels, Face Towels, Towel Bundles, Shop all) + **3 promo image tiles** (each up to 300px wide, ~230 tall, white caps label centred: "NEW IN - FOREST PINSTRIPES", "SHOP TOWEL BUNDLES", "SHOP FACE TOWELS").
  - **Life & Lounge**: Heavyweight Tees, Loungewear Women, Loungewear Men, Loungewear Shop All, Totebags, Pet Quilts + 2 promo tiles. **Home & Living**: Throws, SOJAO x Postcard, Cushion Covers, Table Cloth & Napkins, Shop all + 2 promo tiles.
  - Pattern = category list left, big photo promos right. There is no "shop by brand" in the nav (brands only appear on the stores page).
- **Mobile (390)**: header 85px; hamburger (left) + search + centred SOJAO + cart; **under the header sits a horizontally scrolling text row of the top links** (Bedding, Bath, Life & Lounge, Home & Living, Last Call!...) overlaid on the hero. Hamburger opens a **floating white rounded-corner drawer** (inset ~8px, 374x~830): X circle + "Search" top, links in 22px serif (Bedding > / Bath > / Life & Lounge > / Home & Living > with grey circular chevrons; Last Call!, Gift Cards, Journal plain), social icons + "SGD $" + "Account" at bottom. Chevron drills into sub-panel (INFERRED). 13-mobile-menu.png.

## 4. Pages (1440 wide; y / height from DOM)

### 01 Home (4447px tall) - 01-home.png, 11-home-mobile.png
| # | Section | y / h | Layout & content | Image treatment |
|---|---|---|---|---|
| 0 | Announcement | 0 / 42 | marquee | - |
| 1 | Header | 42 / 74 | overlays hero (transparent) | - |
| 2 | Hero slideshow (`slideshow-carousel`, `transition=fade_with_text`, `autoplay=20`) | 42 / 858 (100vh - 0) | full-bleed video, 3 slides (3 vertical dots right, x1344, active = elongated pill). Text bottom-centred: serif 48px white headline "Organic Heavyweight Tees", white 16px sub "A SOJAO x Dirtydoodies exclusive", navy square "SHOP NOW" button 177x60. Slide 3 headline "Our bestselling sheets, in the all new B..." | autoplay muted looping MP4; separate mobile (portrait 0.667) video; ~15s per slide measured |
| 3 | Scrolling text strip | 900 / 56 | marquee (15.3s linear) of 3 phrases: "Visit us in stores / Find your perfect match / Join the Sleep Easy Club" - each is a link, 16px ink, no separators | - |
| 4 | **What's New** carousel | 956 / 676 | centred serif H2 40px navy; horizontal product slider (4.3 visible, peeking; cards 318 square, gap 24); NEW circle badges | grey tile bg; hover swaps to 2nd image (see 5); swatches below |
| 5 | **Build Your Set** (custom `jsc_set_builder`) | 1632 / 753 | cream `#F2F0EB` band; 2 cols (657 left / 657 right, 48 margin). Left: eyebrow "CREATE YOUR DREAM BEDROOM", serif H2 "Build Your Set", sub, "PICK YOUR SET:" then **Flickity tab cards** (Duvet Bundle Set - SAVE 13%, Quilt Bundle Set, Fitted Sheet Set - SAVE 8% ...; 196x175, white card, 1px border, selected = pale-blue bg + navy border, line-drawing icon of the bundle contents), big navy CTA "BUILD YOUR DUVET BUNDLE SET ->", then white **Sleep Easy Quiz** card (sparkle eyebrow, serif "Let us find your perfect match!", outline button "TAKE QUIZ ->"). Right: tall product-set render (657x657) with a "FEATURED: Duvet Cover: Crisp Barley / Fitted Sheet / Pillowcase Pair" caption overlay | image swaps with selected tab (INFERRED) |
| 6 | **Bestsellers** tabbed | 2385 / 756 | serif H2 "Bestsellers" centred; underlined text tabs BEDDING / PLUSH TOWELS / LIFE & LOUNGE (16px 700 uppercase, active navy w/ 2px underline, others lighter); same product slider | - |
| 7 | **In Your Space** (Instagram/UGC, Instafeed app) | 3140 / 486 | serif H2 centred, then a 6-up edge-to-edge photo strip (296 tall, tiles ~224 wide, 2px white gaps, tiny tag icon top-right) | portrait lifestyle photos |
| 8 | **Pledge band** | 3626 / 241 | full-bleed cotton-boll photo faded to white; left illustrated navy flower sprig; serif 48px two-line statement "Our sheets are ethically-made and organic, with people and planet in mind" (second line in sans bold) + underlined link "pledge to sustainability" | image-with-text over bg |
| 9 | Footer | 3868 / 580 | see 7 | - |

### 02 About - /pages/about (5169px) - 02-about.png
1. Hero image (116 / 669): full-bleed bedroom photo (rust sheets), serif white title "Better Sleep" + sans bold "for everyone" centred-left.
2. Our Story (784 / 1001): 2-col, portrait of two founders left (~636x900 grey tile), right serif "Our Story" 40px navy + 15px body paragraphs, sign-off "Pris & Jan, Co-founders of SOJAO".
3. Name meaning (1785 / 669): full-bleed outdoor washing-line photo; centred serif "SOJAO" + one-line caption ("Means 'go to sleep' in Hindi...").
4. Seed-to-sheets video (2454 / 810): full-bleed muted looping video (farmer holding cotton), small white caption bottom-left.
5. "It's All In The Details" (3264 / 551): 4-col icon grid - hand-drawn navy/rust line illustrations (~110px), serif 24px titles ("Free from nasties", "Longer for better", "300 is all you need", "Built to Last"), 15px copy.
6. "Ready to go organic?" Bestsellers (3815 / 774): eyebrow + serif H2, **3-up** product grid (cards 432 wide).
7. Footer.

### 03 Collection - /collections/classic-bed-sheets (11931px, 51 products on one page) - 03-collection.png
1. Banner (116 / 215): no image - plain white, serif H1 **80px** ink "Classic Sateen" centred, 16px description with underlined inline links to sub-collections.
2. Sub-collection tile row (331 / 298): 6 image tiles (204x238, 24 gap) with bottom-left white label ("Duvet Bundle Sets" ...), no radius.
3. Main (629 / 7734): **left filter sidebar** (~288px: "Filters" icon, collapsible "Product type" with 2-col icon-tile chips drawn as line icons, "In stock only" toggle, Size / Color / Price collapsibles, 1px dividers) + **3-col product grid** (316px cols, 48px row / 24px col gap, x396/736/1076). "Sort by: Featured v" top right. A **promo tile is injected in the grid** (position 5: orange-pillow photo, "Find your perfect match / Sheets Quiz (>)" white overlay, 316x416).
4. Image-with-text overlay (8363 / 719): collection SEO copy on photo.
5. Feel/Temperature/Durability (9082 / 586): 3-col text-led "What does Classic Sateen feel like?" block with 3 images.
6. FAQ accordion (9668 / 909): "What is organic cotton?", "difference between Sateen and Percale", "How to wash bed sheets?" ...
7. Ready-to-go-organic 3-up bestsellers (10577 / 774).
8. Footer.

### 04 Product - /products/classic-natural-duvet-bundle-set (9198px) - 04-product.png, 12-product-mobile.png
1. Main (116 / 1382): 2-col. Left (583px) **sticky gallery** (`position: sticky; top 110px`): vertical 64px thumb rail + large 503 square image on grey tile (6 images incl. lifestyle). Right (713px, x679): serif H1 48/52.8 "Classic Natural Duvet Bundle Set", price 16px + right-aligned rust star rating "279 Reviews" (Yotpo), "This bundle contains:" 3 mini-cards (image + name), "Size Guide" link, "Color: Natural" with **12 round 26px swatches** (selected ring), square-cornered Size `<select>` (full width, 1px ink border), blurb, full-width navy "ADD TO CART" (~60px), underlined "Chat with us", collapsible rows Details / Wash Care (1px dividers, chevron), then "Pair this perfectly with" list of 3 rows (thumb, bold name, price, grey "+ ADD" button). Right column `safe-sticky` top 0.
2. USP icons (1497 / 578): 4 photo tiles (318 square) with centred navy captions: Labeled sides / Envelope closure / Corner ties / Reusable dustbag. Serif H2 "Why you'll love these sheets".
3. **Scroll-driven features** (2076 / 2149, `images-and-text-scrolling`): left column of 3 text blocks (mono "-- 01" counter with short rule, serif 60/66 title "Ultra-soft and buttery smooth", 15px body) scrolls while the right image (684px tall, sticky `top:94px`) stays; 3 images are stacked in one wrapper and **cross-fade in cumulatively** (MEASURED opacity 1/0/0 -> 1/1/0 at ~+300px -> 1/1/1 at ~+1050px; text blocks 2/3 start `opacity-0`). JS-driven, no library.
4. Icon strip (4225 / 425): cream band, 4 illustrated icons + serif titles (Sustainably Made / Easy Care / Softer with Use / 30-Day Returns).
5. Reviews (4650 / 2522): "As heard from you" - 4.9 big rating, bar breakdown, "Write A Review", AI "Customers say" summary, review list (Yotpo widget).
6. FAQ "In case you were wondering" (7172 / 602) accordions.
7. Recommendations (7774 / 844): serif H2 + 4-6 card slider.

### 05 Journal index - /blogs/house-to-home (8324px) - 05-journal.png
Hero (116 / 324): solid **rust `#BA5028`** block, serif white "We Hustle Hard" + bold sans "Just like you", centred; then blog tabs sit on the hero bottom edge (House To Home active = white tab with ink text; How Tos / She-Hustles / Ultimate Bedding Guide = ink text on rust). Then **3-col portrait-card grid** (cards ~396 wide, 4:5 image 396x526, 24px gap, 72px row gap): serif 28px title, 15px 4-line excerpt, no date. 7305px of 50 images (no pagination seen; INFERRED lazy/infinite or long page). Four blogs total: House to Home, How Tos, She-Hustles (founder profiles), Ultimate Bedding Guide.

### 06 Journal article - /blogs/house-to-home/ochrehome (22590px) - 06-article.png
Serif H1 ~64px centred full width ("An Eclectic Art-Filled Home With Hygge"), small calendar-icon date, full-width 16:5 hero image (1344 wide), then a 2-col body: narrow ~750px text/image column (bold eyebrow "HOUSE TO HOME #02", italic names, rust underlined IG handle, big lifestyle photos interleaved with pull quotes) + **right sticky "Featured in this post" card** (cream bg, 2 shoppable product cards: Classic Autumn Duvet..., sale price in rust with strike-through). Ends with "Reading next".

### 07 Stores - /pages/our-store (2573px) - 07-stores.png
**Alternating 50/50 split blocks, full-bleed, no gutters**: (1) storefront photo left / **solid navy `#29378C`** panel right: eyebrow "VISIT US IN THE EAST", serif white "Joo Chiat Road", address (underlined), opening hours, bullet list "Shop these brands in-store" (Studio Yono, Hush Candles, State Of Matters, Sardine, Stillgoods, ... 14 brands); (2) mirrored: navy panel left "New Bahru" / interior photo right (white pendant-lamp / bedding shelving). Then rust band "SOJAO Store Vendor (Expression of Interest)". Panel heights ~820px each. No map, no embedded form seen. Note: they stock other brands' home goods (lamps/planters/candles) in store - relevant to a lighting concept.

### 08 Rewards / Sleep Easy Club - /pages/rewards (4281px) - 08-rewards.png
Account sub-nav bar (Rewards / Orders / Addresses / Login, tint `rgba(10,39,61,.05)`), Yotpo Loyalty embed: polaroid-flatlay hero with serif title + JOIN NOW (navy) / LOGIN (white) buttons, "Get Started" 3 numbered circular step badges (rust 1 / navy 2 / yellow 3), "Ways to Earn Points" 3x2 cream-tile grid with line icons. Largely third-party widget styling; low copy value.

### 09 Category landing - /pages/bedding (4289px) - 09-bedding-landing.png
Serif H1 "Shop All Bedding" + paragraph (116 / 187); then **4 alternating zig-zag rows** (each ~460-560px tall; image 936x ~460 full-bleed to one edge, text column with serif 40px navy title, 15px copy, navy "SHOP CLASSIC SATEEN"-style button; the "Mix & Match" row uses a **rust button** "BUILD YOUR PERFECT BEDROOM"); FAQ accordion; "Looking to find your Perfect Match? TAKE OUR SHEETS QUIZ" band. This is the pattern behind the nav's "Shop Bedding" CTA.

### 10 Quiz - /pages/take-our-quiz (1487px) - 10-quiz.png
Cream page, centred hand-drawn navy+rust illustration (person sleeping), serif H2 "Take our Sheets Quiz", sans sub, small navy "Start Quiz" button; quiz itself = RevenueHunt app overlay (not captured).

Pages not captured as separate screenshots (cap 10): /pages/sustainability, /pages/faq, size-guide pages (`/pages/fitted-sheet-size` etc. - ~30 spec pages), /pages/careers, /pages/wash-care, /collections/all, Cart page, search drawer. **No separate "projects / lookbook / contact" page**: Journal "House to Home" is the lookbook equivalent; Contact = `/pages/faq#contact-us`; stores = /pages/our-store.

## 5. Animations / interactions
| Where | Effect | Trigger | Detail | Evidence |
|---|---|---|---|---|
| Product card | **Image swap on hover** (primary 1 -> 0, secondary 0 -> 1, both square 318) | hover | `opacity .2s ease-in-out`; no zoom/transform | MEASURED |
| Card quick-add | "ADD TO CART" bar appears over image bottom on touch/mobile card; desktop not confirmed | - | seen in mobile screenshot | observed |
| Buttons | bg -> navy@.85 | hover | .15s ease-in-out | MEASURED |
| Nav links | 1px underline slide-in | hover | transform .25s ease-out | MEASURED |
| Mega-menu | opens on hover, full-width white panel, rest of page dimmed 40% (box-shadow) | hover | `transition: all`, panel appears ~instantly | MEASURED (open-state shadow), timing INFERRED |
| Hero | 3-slide fade_with_text slideshow; video bg; dot pagination right | auto 15-20s / dots | `autoplay=20` attr; sampled change between 12s and 15s | MEASURED |
| Announcement bar | endless marquee 39.9s linear | time | | MEASURED |
| Strip below hero | endless marquee 15.3s linear | time | | MEASURED |
| Product list carousels | Flickity-style drag/scroll with peeking next card (Set Builder tabs = Flickity: no wrap, draggable, no arrows) | drag/arrows | | MEASURED (set builder), others INFERRED (scroll-snap) |
| Product page | sticky gallery (top 110) + scroll-driven image cross-fade section | scroll | JS, no lib | MEASURED |
| Scroll reveals / parallax / cursor / zoom | Not detected beyond `reveal-on-scroll` on slideshow. No parallax, no custom cursor, no GSAP | - | negative evidence | MEASURED lib absence |

## 6. Footer (all pages; 580px, bg `#F2F0EB`)
- Left block: rust serif "Sleep Easy Club" 48px, bold caps sans "WE HUSTLE, YOU SLEEP EASY", 15px copy ("Get 5% off your first order. Collect points ... rewards program."), navy "JOIN US" button (54px) - this is the newsletter/loyalty signup (links to /account/register, no email field).
- 3 link columns (12-13px bold caps heading, 15px grey links, ~38px line spacing): **SHOP** (Shop Bedding, Bath, Loungewear, Home Decor, Gift Cards, Size Guide) / **ABOUT** (Our Story, Sleep Easy Club, Sustainability, Journal, Visit Our Stores, Careers) / **HELP** (FAQ, Shipping & Returns, Privacy Policy, Contact Us, Sheets Quiz, Wash Care, EU Withdrawal).
- Bottom row: Facebook, Instagram, Pinterest, TikTok icons (22px, ink) left; country/currency selector "SGD $" with flag right; (c) 2026 SOJAO left; payment icon row right (Amex, Apple Pay, GPay, Mastercard, Shop, UnionPay, Visa). A separate Thailand storefront link (sojao.co.th).

## 7. Overlays
Klaviyo newsletter popup + Yotpo loyalty launcher + Hotjar surveys can appear on first visit (stripped for screenshots). Search opens as a drawer (`search-drawer` section). Cart = `/cart` page link plus cart.js.

## 8. Borrowable for a lighting concept store
1. **Hover-triggered full-width mega-menu with list left + big image promos right**: panel y116, white, page dimmed `0 0 0 9999px rgba(0,0,0,.4)`; column titles 24px accent colour, links 16px; promo tiles 172-300px wide, ~230px tall, white 14px bold caps label centred over photo. Map: columns = Pendants / Table / Floor / Wall / Outdoor; promos = "New In", "Warm 2700K", "By room".
2. **Transparent header over full-bleed video hero -> solid white sticky on scroll** (74px, logo white->accent). Hero = 100vh, centred serif 48px title + 16px sub + 177x60 square button; 3 slides, vertical dot pager right edge, ~15-20s autoplay, separate portrait mobile video. For lighting: day-to-dusk video loops.
3. **Restrained 2-colour + cream palette**: ink `#0A273D` + one saturated accent `#29378C` + one warm secondary `#BA5028` + cream `#F2F0EB`. All text/heading/button in the accent; sharp 0px corners. Reads gallery-like.
4. **Serif display + clean sans body**: Poynter-style old-style serif 500, tracking -0.02em, line-height 1.1, sizes 40 (H2) / 48 (hero, PDP) / 80 (collection H1); Instrument Sans 16/1.6. Free alternatives: a similar old-style display serif (e.g. Fraunces / Newsreader) + Instrument Sans.
5. **Square product tile + hover second-image swap** (opacity .2s) on a light-grey `#E5E5E5` tile, centred title/price, round colour swatches (26px, `+N` chip) - for lighting, swatches = finish (brass/black/opal). Grid 3-col with 24px/48px gaps beside a left filter rail; inject a **promo tile** into the grid (quiz/lookbook) at position 5.
6. **Configurator "Build Your Set" band**: cream band, 50/50, tab cards (196x175, icon + save-badge + 2-line copy) driving a big render on the right + navy CTA + secondary "Take quiz" card. Adapt to "Build your lighting scene" (room -> fixtures set with bundle discount).
7. **PDP: sticky gallery (top 110px) with thumb rail + sticky buy column**, "bundle contains" mini-cards, "Pair this perfectly with" +ADD rows, accordion Details/Wash care, full-width navy ADD TO CART. Good for lamp + bulb + dimmer cross-sell.
8. **Scroll-driven features block**: sticky 684px image (top 94) + 3 scrolling text blocks (mono "-- 01", serif 60px title); images stack and cross-fade cumulatively. Highly relevant: show a lamp at 2700K -> 3000K -> 4000K as you scroll.
9. **Alternating 50/50 solid-colour panel + photo store page** (navy panel with white serif name, address, hours, brand list; photo opposite; no gutters; ~820px blocks) - best-in-class "visit us" pattern for a physical showroom; list the brands you stock.
10. **Hand-drawn line-illustration icon grids** (navy + one rust accent) for "It's all in the details" (4 cols, 110px illus, serif 24 title, 15px copy) and on cream strip. Distinctive vs stock icons; commission lighting equivalents (filament, shade, dimmer).
11. **Journal = home tours, shoppable**: rust full-bleed hero + tabbed blog filters; 3-col portrait cards (4:5), serif 28px titles; article has a **sticky "Featured in this post" product card** on the right. Strong for "house to home" lighting stories.
12. **Dual marquees**: announcement strip (rust 16px, bullets, 40s) + CTA text strip under hero (15s, 3 links). Cheap, effective.

### Generic / not worth copying
- Impact-theme boilerplate: tabs under "Bestsellers", centred H2 + horizontal slider, FAQ accordions, 4-col footer, "Sleep Easy" rewards (Yotpo) page, Yotpo/Klaviyo popups - template Shopify, no distinct design.
- Third-party widgets (reviews, loyalty, quiz overlay, Instafeed) look off-brand/default.
- Home "In Your Space" UGC strip is small and unlinked-looking; rewards page has dated Yotpo styling.
- Heavy script load (Klaviyo/Hotjar/Clarity/Yotpo/Elevar) - slow (networkidle never reached in 60s); don't replicate.
- No scroll-reveal polish, no GSAP, no smooth-scroll: the site is static-feeling except for videos and marquees - the "premium" feel comes from photography, serif type and the colour palette, not motion.
- Colour caveat: heavy ultramarine navy + rust is a SOJAO brand signature; copy the *structure* (1 accent + 1 warm + cream + ink), not these exact hexes, if you want a distinct identity.
