# Etsy Digital Product: 2027 ADHD Planner 🌿

Is repo mein Etsy par digital product bechne ke liye sab kuch tayyar hai: research, keywords, product files, listing images, listing text aur promotion plan.

| Step | Status | File |
|---|---|---|
| 1. Etsy research | ✅ Done | `research/market-research.md` |
| 2. Account create | ⏳ **Aap ko khud karna hai** (neeche guide hai) | yahi README |
| 3. Digital product find | ✅ **2027 ADHD Planner** (printable PDF) | `research/market-research.md` |
| 4. Keywords | ✅ Done (Ahrefs + Etsy autocomplete) | `research/keywords.md` |
| 5. Product create | ✅ 26 pages, US Letter + A4 | `product/output/` |
| 6. Host (Etsy listing) | ✅ Title, tags, description, 8 images ready | `listing/` |
| 7. Promote | ✅ 30-day plan, Pinterest pins, video ideas | `promotion/promotion-plan.md` |
| 8. Earning | ⏳ Shop live hone ke baad | |

## Kyun yeh product?
- Abhi **October** hai, aur log 2027 ke planners **Oct-Jan** mein sab se zyada khareedte hain.
- "adhd planner" ki **6,400 searches/month** hain aur competition kam hai (KD 18). "habit tracker printable" bhi 6,400/month hai (KD 2).
- Banane mein koi kharcha nahi aur koi shipping nahi, profit lagbhag **$5.58 per sale** ($6.99 par).

---

## Step 2: Etsy account aur shop khud banayein (lagbhag 30 min)
Main aap ka account nahi bana sakta. Is ke liye aap ki ID, bank/Payoneer, phone aur email verification chahiye, jo sirf aap kar sakte hain.

1. **Payoneer account** banayein: payoneer.com par jayein aur CNIC + bank details dein. Approval mein 1-3 din lagte hain. Pakistan mein Etsy ki payouts Payoneer ke zariye aati hain.
2. **etsy.com/sell** par jayein, phir **Get started** par click karein aur email se account banayein.
3. Shop preferences mein: Language English, Country **Pakistan**, Currency **USD**.
4. **Shop name** chunein: **FocusNookPrints** (19 Oct 2026 ko khaali tha).
5. **First listing** banayein. Neeche "Listing upload" dekhein.
6. **Payments**: Payoneer connect karein.
7. **Billing**: debit/credit card add karein. Is se listing fee ($0.20) aur shop setup fee (agar lage) kategi.
8. **Security**: 2-step verification ON karein.
9. Shop open karein. ID verification maange to CNIC ki photo upload karein.

## Step 6: Listing upload (copy-paste)
1. Shop Manager → Listings → **Add a listing**
2. **Photos**: `listing/images/01-hero.jpg` se `08-how-it-works.jpg` tak, isi tarteeb mein
3. **Title, tags, description**: `listing/etsy-listing.md` se copy karein
4. **Type: Digital**. Phir yeh dono files upload karein:
   - `product/output/2027-ADHD-Planner-US-Letter.pdf`
   - `product/output/2027-ADHD-Planner-A4.pdf`
5. **Price $9.99**, phir Marketing → Sales mein **30% off** lagayein (buyer ko $6.99 parega)
6. **Publish** karein 🎉

## Step 7: Promote
`promotion/promotion-plan.md` kholein. Roz 3-5 Pinterest pins aur 1 short video post karein. Pin image `listing/images/pinterest-pin.jpg` hai.

## Earning: sach baat
Pehli sale aam tor par 2-6 hafte mein aati hai. Har hafte naya product add karein (list `research/keywords.md` mein hai). Lagbhag 20 listings aur reviews ke baad 1-5 sales/day mumkin hain. Lekin yeh **guaranteed nahi**, yeh consistency par depend karta hai.

---

## Files regenerate karna (agar design badalna ho)
```bash
python3 product/scripts/build_planner.py product/output
python3 product/scripts/build_listing_images.py product/output/2027-ADHD-Planner-US-Letter.pdf listing/images
```
Requirements: Python 3, `reportlab`, `Pillow`, `pdftoppm` (poppler-utils). Colours aur pages `build_planner.py` ke top par badal sakte hain.
