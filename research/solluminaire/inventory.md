# solluminaire.com.sg inventory (measured 2026-10-26, isolated headless Chromium 1440x900 and 390x844)

Method: Python Playwright scripts (p*.py, probe*.py in this folder), computed styles from the live DOM. AOS scroll-reveals were force-completed with injected CSS before full-page screenshots, so screenshots show the final state. Sol Luminaire is a Singapore lighting brand/distributor with 4 showrooms. It is a CATALOGUE/EDITORIAL site, not a cart store: no cart, no checkout; spec sheets + WhatsApp enquiry. (Only the "View All / Archives" page shows prices.) Confidence: M = measured, I = inferred.

## 1. Tech signals
| Item | Finding |
|---|---|
| Platform | WordPress + Oxygen Builder (body class `oxygen-body oxygen-aos-enabled`, `ct-section`, `ct-div-block`), Oxy Extras mega menu, WP Grid Builder (filters/pagination on View All), Fluent Forms (newsletter), SiteGround cache + lazysizes, Site Kit by Google (M). Built by terris.sg |
| Animation | AOS (Oxygen's bundled) only: `data-aos=fade-in`, duration 800ms, easing ease-in-sine, offset 150, once=false (re-fades on scroll back up) (M). No GSAP/ScrollTrigger, no Lenis/smooth-scroll, no Lottie (M, typeof checks). Parallax script `parallax.min_.js` is loaded (no visible use found) |
| Carousels | Flickity 2 (jQuery) on product + gallery image strips: `cellAlign center, friction .28, selectedAttraction .025, prevNextButtons false` + custom gold round arrow (`next-icon-hover.svg`), draggable only when >1 cell (M) |
| Video | 3 `<video autoplay loop muted playsinline>` on home: hero `web-banner-3.mp4` (13.1s, 1440x831, object-fit cover, wrapped in link to /coming-soon/), Dark Room clip (634x343), Nocte clip (599x1064, object-fit contain). No GIFs except loading-indicator.gif (M) |
| Fonts | Addington CF v1.7 (serif, self-hosted woff2 Thin+Regular; used at 400/500) for everything; "Snake" handwriting font for home accent labels; Rooms page: Jeff Script + Giuconda. Cirka and Copperplate files are also fetched (not seen in use on probed pages). Google Archivo is declared but unused (M) |
| Other | GTM + GA + Meta pixel; round-slider lib (price filter); preloader div `.oxy-preloader` (hidden after load); WhatsApp floating button |
| Popup | Oxygen modal "Lights & Luminaries" newsletter, top-right card, opens 1s after load, shows again after 1 day; scrim rgba(196,196,196,.6). Dismissed via X for all screenshots (M) |

## 2. Global design tokens
| Token | Value (M) |
|---|---|
| Body font | Addington CF, 16px / 25.6px, 400, colour #404040, letter-spacing normal |
| Ink / headings | #0F0F0F (near-black); nav links #000 |
| Page bg | #FFFFFF everywhere. No dark sections, no cards, no shadows, 0px image radius |
| Accent | gold/sand rgb(222,195,150) #DEC396 - pill buttons, WhatsApp bubble, carousel arrows, "Reset Filters" pill. Logo ring is a bright yellow (#F5C518-ish, I). Page-specific highlights: neon yellow rule + squares in Rooms/Nocte creative (brand-supplied) |
| Typography scale | Extremely small and quiet. Card titles/H2 on home: 15.632px/23.45 400. Small copy 11-13px (contact/about body 13px/20.8; contact lines 11px/17.6 weight 300). Page titles: 19.2px/24.96 centred, capitalize. Section heads: 20px/32 500. Pull quote: 32px/38.4 500. Story list title 32px/51.2 500; single story H 41.168px/53.5. Product title 41.168px/53.5. Eyebrow/category: 15.6px rgba(0,0,0,.5). Letter-spacing is `normal` throughout except buttons (0.5px). No uppercase eyebrows except "DISCOVER MORE" |
| Container | `ct-section-inner-wrap` max-width 1140px (about, product) or full 1440 with 20px gutter (collection/stories/gallery/contact/home) |
| Section padding | 75px 20px typical (top/bottom); home content section 125px top, 75px bottom; product section 75 top, 150 bottom; footer 75px 20px |
| Grid gaps | home 2-col 688.5px, gap 63px; collection 4-col 327.5px, gap 30px; stories 2-col 646px, gap 108px; gallery 4-col 269px, gap 108px; view-all 4-col gap 30px; contact 2x(2) 63px |
| Button | pill, border-radius 9999px, bg #DEC396, text #000, 16px, ls 0.5px, padding 4px 35px, height 34px, no border. Footer Subscribe = ghost pill: 1px solid #000, transparent, 11px, ls .5px, 4px 35px |
| Inputs | underline only: border-bottom 1px #000, no box, placeholder "Email Address" ~11px |
| Radii | 0 on all imagery; 9999px on buttons/selects/filter pills only |

## 3. Navigation
- **Announcement bar**: none (M).
- **Header**: 76px, padding 17px 20px. Logo (101x35 yellow ring + "Sol Luminaire" wordmark) top-left at x=20; nav links start x=161 left-aligned beside logo (not centred); search icon (16px) far right at x~1412. Optional extra links appear on some pages (collection pages showed bold "Sale" after Contact and a gradient-animated "Professional" at far right) (M).
- **Top-level links, in order** (14px/400 black, ~70px pitch): About, AEON(R), Sol-T, Gallery, Stories, Rooms, the LAB2.1, Galerie 5, View All, Coming Soon, Dark Room (external subdomain darkroom.solluminaire.com.sg), Contact. 12 links, a deliberately flat "everything on one row" nav.
- **Sol-T** link text has an animated gradient (`gradientFlow 12s ease-in-out infinite`; linear-gradient(270deg,#95CFF1,#95CFF1,#FFFEFD,#F2C072,#F2C072)) so it slowly cycles blue -> white -> amber (M). Same trick on "Professional".
- **Behaviour**: overlay header - transparent over the home hero video at y=0, then goes `position: fixed`, white bg, fades in (0.5s linear) once you scroll (class `oxy-sticky-header-fade-in`); it scrolls out of view first then reappears (M). On inner pages the bar is white.
- **Mega menus = HOVER-open** (Oxy Extras), full-width white panel at y=54 (overlapping header), 0.5s transition, no scrim. Content measured:
  - **AEON(R)** (369px tall): 3 image tiles (~322x258, 4:5-ish landscape crop) with caption below: Circuit.11 Track System, Indoor, Outdoor -> tag archives.
  - **Sol-T** (340px): text columns: All Products, Super Smart Panels / Switches / Dimmer Switches / Accessories, Kinetic Switch, About + one image.
  - **Stories** (347px): 4 image tiles (236px tall) The Edit / Lights On / In Conversation / Sol Meets + "All Stories/" link.
  - **Rooms** (430px) = BRAND DIRECTORY: 3-column list, each cell = brand name (small bold-ish) + product-type sublinks: AEON(R) (Circuit.11, Indoor, Outdoor), Rooms (Dotti and Pixxi, Pulp), LYFA (Luminaires), Market Set (Luminaires), Hansgrohe (Bathroom and Kitchen Fixtures), KKPL (Home and Wardrobe Accessories), Noble surfaces (Textured Wall Finishes), Oculus Collective (Signature Glass Door), Ornate+ (Glass Bricks and Foam Ceramics), Spin fans (Ceiling Fans), Caerus Electric (Simon Switches), About; plus "Rooms: The Virtual Tour" and one tall image on the right (312x250). Type 11-12px.
  - **the LAB2.1** (340px) and **Galerie 5** (355px): same brand-directory pattern (LAB: Boba Pendant, Boba Chain, Perforated Boba, A Emotional Light, Buster+Punch (Hardwares / Switches / Luminaires), Eshen Ceramics, Mad et Len Fragrance...; G5: LYFA, LLLL, Makhno Studio, Forma Rosa Studio, Sklo, Lightmass, furniture studios, Natura Ceramica, Sticky Glass...). Each brand heading links down to a brand page `/product_archive/<brand>/` or `/single-post/sol_g5_arch/<brand>/`.
  - About, Gallery, View All, Coming Soon, Dark Room, Contact = plain links.
- **Search**: icon toggles an Oxygen search form (overlay not captured; I).
- **Mobile (390px)**: header = logo + search icon + 20px burger (hamburger -> flat dropdown). Menu opens as a plain white list directly under the 69px bar (553px tall, 14-16px links, ~42px row pitch, left-aligned 15px, no dividers, no accordion visible at top level; sub-menus presumably nested - not opened). No horizontal overflow (scrollWidth 390) (M). Screenshot 13-mobile-menu.png.

## 4. Pages
Pages visited: home, about, gallery, stories (listing), single story, product (Goli), collection (/product_tag/indoor-lighting/), view-all (Archives), contact, rooms. Brands page: exists only as the "Rooms / LAB2.1 / Galerie 5" brand-directory pages and brand archives (not visited individually except rooms). Services page: the About page contains "Our Services" + DIALux sections (no separate page). Projects: the Gallery page is a project/portfolio listing. Also exist (not shot): about-sol-t, the-lab2-1, galerie5, coming-soon, darkroom subdomain, privacy-policy.

### 4.1 Home (01-home.png, 4553px tall at 1440; mobile 11-home-m.png 4334px)
| # | Section (y, h) | Content / layout |
|---|---|---|
| 0 | Header 0, 76 | overlay header |
| 1 | Hero video 76, 831 | Full-bleed autoplay muted looping video (object-fit cover), no text overlay, whole thing links to /coming-soon/. No scroll cue. |
| 2 | Editorial stagger grid 907, 3346 (inner pad 125px top / 75 bottom) | 2-col grid (688.5px each, gap 63) with items deliberately offset so the layout is irregular: (a) left y=1032: "Experience / Dark Room" label (15.6px) + 634x343 autoplay video + footer row "Experience ........ Here"; (b) right y=1032: "AEON(R) / Goli" + tall portrait image (~629x960) + row "Discover ........ Goli"; (c) left y=2059: "AEON(R) Evolution" in Snake handwriting + 599x1064 vertical Nocte video (contain on #F0F0F0) + row "Discover ... Nocte" in Snake 27.2px; (d) right y=2134: circular rotating-style "What is New?" hand-drawn SVG badge 108x93 right-aligned, links to /coming-soon/; (e) left y=3541 (right-padded 140): "The Edit/ Market Set arrives..." + landscape image bleeding to the left viewport edge + "Read ........ Here"; (f) right y=3091 (pad-left 115): "DISCOVER MORE / 30mm" + tall image bleeding to RIGHT viewport edge + "Discover ... 30mm". |
| 3 | Footer 4253, 300 | see section 6 |
Image treatment: no radius, no overlay, no captions on image; caption sits ABOVE (title, 15.6px) and BELOW (action word left, product name right, same 15.6px baseline, justified row). All media links to page. Images switch alignments left-edge / gutter / right-edge to create rhythm.
Mobile: everything collapses to a single column, hero ~390 wide full video, same title-above/label-row-below pattern, badge centred (measured on 11-home-m.png).

### 4.2 About (02-about.png, 3253px)
Narrow 835px centred column (1140 wrap, 20px gutter). 1) y76-681: 2-col [405 | 350] gap 40: showroom photo (345x431) left, right "About" 20px/32 500 + 13px/20.8 body (4 paragraphs). 2) y681-883: large pull quote 32px/38.4 500 "There's a saying 'home is not a place but a feeling'..." 3) y883-1229: image collage, 2 images overlapping/offset (179x250 and 268x376) in a 318|477 grid. 4) y1229-1802: "Our Services" 20px + body left, 2 stacked wide images right (278x160, 278x188). 5) y1802-2253: "DIALux" heading + body right. 6) y2252-2953: "As Seen On" - 5-column logo wall of press logos (63x63 tiles, 9px gap, 25 logos, colour tiles: CNA, Tatler, d+a, Lookbox, Cubes, SquareRooms, etc.). Footer 2953.

### 4.3 Gallery (03-gallery.png, 2705px) - project portfolio
Single full-width section, 4-col grid of Flickity cells (269px wide, gap 108px, image 269x403 portrait or 269x269 square, each is a swipeable carousel of that project's photos with gold arrows). Caption above in 16px/25.6 #404040: "Studio / Location" (e.g. "Typeface/ 97 Hougang", "Freight Architects/ Siglap Close"); 16 projects in 4 rows, row pitch ~572px. No filters, no page title.

### 4.4 Stories listing (04-stories.png, 6623px)
2-col grid (646px, gap 108px), 12 articles, row pitch 1030px. Card: category eyebrow (15.6px rgba(0,0,0,.5), e.g. "The Edit" / "Lights On" / "In Conversation" / "Sol Meets") at y+2, title 32px/51.2 500 (2-3 lines), then a large portrait image (646x~800), then 16px excerpt line under the image. Cards are AOS fade-ins.

### 4.5 Single story (05-story.png, 5901px)
Category 16px at 50% opacity; H1 41.17px/53.5 400; intro 16px #404040; then long-form editorial: images full width with "Pictured above:" captions (15.6px, em) and body text in a narrow ~590px column offset to x=430. 5901px tall.

### 4.6 Product page - Goli (06-product.png, 1465px; mobile 12-product-m.png 2152px)
Section 1 (y150-640): 2-col, left square-ish image 519x415 (grey ceiling photo), right column x=752: H1 "Goli" 41.17px/53.5 400; tagline 15.6px "A marble. A lens. A light."; ~120px gap; description paragraph 15.6px/23.4 (4 lines); gold pill "Product Details" (181x34) which reveals the spec tables. Section 2 (y715-1210): Flickity strip of variant photos: portrait 375x450 + landscape 705x450 side-by-side, 20px gap, with gold circular arrow (right, 50x50) beside. Spec tables (revealed): per-variant H2 (20px 500, "Goli U&D", "Goli Adjust") + 2-col table label (15.6px/500) | value (400): Wattage, CCT 1800K-3000K, CRI 90, Lumens, Lumen per Watt, Colour, Product Category, Dimming Compatibility + link "Sol Luminaire Dimming Playbook". No price, no add-to-cart, no related-products rail. Header is hidden (opacity 0) at the top of this page until scroll (M).

### 4.7 Collection - /product_tag/indoor-lighting/ (07-collection.png, 4600px)
Centred page title "Indoor" 19.2px (capitalize) at y76 directly under header, 100px gap, then 4-col grid, gap 30px, cards 328x409 portrait (object-fit cover, studio shots on light grey #D9D9D9-ish bg), name below at 15.6px/23.4 (left-aligned), no price, 30 products, row pitch ~507px. No filters or pagination on this view.

### 4.8 View All / Archives (08-view-all.png, 3375px) - the only transactional-looking view
Title "Archives" 19.2px centred. Filter row (5 equal columns 256px, gap 30): Brand select, Category select, Price range slider ($29 - $14,999) + reset, Sort select ("Featured Products"), Reset Filters pill (gold). Selects are rounded-pill outlines. Then 4-col grid (327.5, gap 30) of 20 products per page: image (mixed crops, 328x468 card), name 15.6px, price 16px ($5,199...). Pagination "1 2 3 ... 25 26 Next". Brands seen: llll (Galerie 5), Slamp-like, KHMARA, Buster+Punch (Hooked), iKinetic.

### 4.9 Contact (09-contact.png, 1532px)
No form, no map. 2 columns (668px, gap 63), left = "Address" H1 (19.2px capitalize) with 5 location blocks (Headquarter; Sol Luminaire Gallery - 395/397 Guillemard Road; the LAB2.1 Gallery - 399 Guillemard Road; Galerie 5 Gallery - 50 Craig Road; Rooms by Sol Luminaire - 400 Balestier Road), each H3 15.6px + 11px/300 address lines. Right = "Contact" with per-location Tel/WhatsApp/email and hours (Mon-Fri 10AM-7PM, Sat 11AM-5PM, Sun closed; Sat by appointment only; Warranty & Services Mon-Fri 9-6). "Whatsapp Us /" text link. Very text-only; row pitch ~130px. Both columns same y-grid.

### 4.10 Rooms (brand/marketplace microsite, 10-rooms.png, 7015px)
Hero: yellow-circled "Rooms" script logo (250x127) centred; hand-script H1 (Jeff Script 48px) "Balestier's modern touch for discerning homes." left-overlapping a 1120x747 interior photo (x160). Intro in Giuconda 19.2px/30.7 500. Thin neon-yellow rule. Then 8 alternating brand rows (sections 455-796px): grid 445|891 with `m-reverse` flipping: script brand-category heading (Jeff Script 32px: "Luminaires", "Simon Switches", ...), brand logo (LYFA, Caerus, hansgrohe, Noble Surfaces, Oculus, Ornate+, KKPL, SPiN), lifestyle photo, blurb in Giuconda 16px/25.6 500 #404040, some blurbs prefixed by a big black quote-mark glyph. Footer same.

## 5. Interactions / animation summary
| Where | Effect | Confidence |
|---|---|---|
| All content blocks | AOS fade-in, 800ms ease-in-sine, offset 150, replays on scroll up (once:false) | M |
| Cards / images (home, collection, stories) | hover: image opacity 1 -> 0.8, `0.5s linear`. No zoom/scale (transform stays none) | M |
| Mega menu | hover open, ~0.5s transition, white full-width panel | M |
| Header | fades in (0.5s linear) fixed white bar after scrolling; transparent over hero | M |
| Sol-T / Professional link | 12s infinite animated 4-stop gradient text | M |
| Hero + 2 home tiles | autoplay muted loop video | M |
| Product/gallery strips | Flickity drag/arrow, no autoplay observed | M |
| Newsletter popup | modal, 1s after load, reappears after 1 day | M |
| Cursor effects, parallax, pinned scrollytelling, page transitions, smooth scroll | none detected | M (negative) |
| WhatsApp floating bubble | fixed bottom-right 50x50, opens wa.me chat pre-filled "book an appointment with your lighting advisors" | M |

## 6. Footer (300px, white, no top border)
Row at y+75: left = 3 black social icons (Facebook, Instagram, Pinterest ~16px, 15px gap) x=20; right = newsletter (x=1079): underline email input "Email Address" + ghost-pill "Subscribe" (1px black border, 11px, 4px 35px) + consent circle checkbox + "I agree to the terms of use. View privacy statement." (11px/300). Below, in white text on white (invisible: bug) "Website by terris.sg". No columns, no link lists, no address/hours in footer, no copyright line. Floating WhatsApp bubble sits fixed over content.

## 7. Screenshots (this folder)
01-home, 02-about, 03-gallery, 04-stories, 05-story, 06-product, 07-collection, 08-view-all, 09-contact, 10-rooms (all 1440w full-page, popup dismissed, AOS forced visible), 11-home-m, 12-product-m (390w), 13-mobile-menu. Tokens: tokens.json.

## 8. Borrowable for a lighting concept store
1. **Whisper-quiet type scale**: serif at 15.6px/23.4 for titles, 11-13px small copy, 16px/25.6 body, only product/story H1 at 41.2px. Hierarchy comes from space, not size. Copy: titles 15.632px/400, ink #0F0F0F, body #404040. Needs a good serif (they use Addington CF; free substitutes: Cormorant/Newsreader/Source Serif light).
2. **Title-above / action-row-below card**: label above the media, then a justified row under it: left verb ("Discover/Read/Experience"), right product name, both 15.6px. Use for all home tiles; it replaces buttons.
3. **Irregular editorial stagger on home**: 2-col grid (688px, gap 63) with items vertically offset by hundreds of px and some bleeding to the viewport edge on alternate sides; reads like a magazine. Home y=907 section, padding 125/75.
4. **Full-bleed muted looping video hero, no copy** (100vh minus header, 1440x831) then immediately editorial grid. Mix looping product videos (634x343, 599x1064 contain) inside the grid.
5. **Hover mega menu with image tiles** (AEON panel: 3 tiles ~322x258 + caption 12px, panel 369px, 0.5s) and **brand-directory columns** for multi-brand shop (brand heading + product-type sublinks, 3 cols, 11-12px, 1 hero image right). Best structure to steal for a "shop by brand" nav.
6. **Pure image grid with name only** for collections: 4-col, gap 30, 4:5 card (328x409 cover) on soft grey studio backdrops, name 15.6px underneath, no price/badges, page title 19.2px centred. Hover = opacity .8 in 0.5s linear.
7. **Spec-sheet-first product page**: H1 41px + one-line poetic tagline + 1 paragraph + gold pill "Product Details" opening a 2-col label/value table (Wattage, CCT, CRI, lumens, lm/W, colour, dimming compat, link to playbook). Then a Flickity image strip (portrait + landscape, 20px gap, gold circular arrow). Ideal for lighting (tech data as the product).
8. **Gold pill + ghost pill system**: sand #DEC396 fill / black text / pill radius / 4px 35px / ls .5px for primary; 1px black ghost pill for secondary; underline-only inputs. One accent colour on pure white.
9. **Animated gradient text for one nav link** (12s, #95CFF1 -> #FFFEFD -> #F2C072): a "light"-themed highlight for a feature link (e.g. Smart/Pro).
10. **Light-themed utility details**: fixed gold WhatsApp bubble with pre-filled "book an appointment with your lighting advisors" message (50x50 bottom-right); consent-checkbox newsletter in a once-per-day top-right modal card.
11. **Project gallery as carousel-per-project**: 4-col grid, each cell a swipeable Flickity carousel, caption "Studio / Location" above in 16px.
12. **Press/"As Seen On" logo wall** (63x63 tiles, 5 columns, 9px gap) and **narrow 835px reading column** for About with large 32px/500 pull quote.

NOT worth copying (generic or flawed): 12-link flat nav in one row (too crowded, no hierarchy); footer with no columns/address/hours and invisible white "Website by" credit; contact page that is only text (no map/form); View All filter bar (default WP Grid Builder selects); modal popup 1s after load blocking first impression; AOS opacity-only fades (generic, and re-fire on scroll up); lack of accessible text size (11px at weight 300 fails contrast/readability); preloader; no scroll cue on the silent hero; Oxygen Builder idioms (c-columns classes). The site does not sell online - copy the catalogue calm, not the lack of purchase path.
