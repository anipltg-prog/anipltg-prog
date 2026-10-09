# Add this README to GitHub

1. Extract `AlphaNumeric-GitHub-README.zip`.
2. Open the extracted `AlphaNumeric-GitHub-README` folder.
3. Copy `README.md` and the entire `assets` folder into the root of your repository. Keep the filenames and folder structure exactly as supplied.
4. Commit and push those files, or use GitHub's **Add file → Upload files** to upload them together. Upload the folder contents, rather than leaving them inside an extra `AlphaNumeric-GitHub-README` folder.
5. Open the repository's main page. The README will display the code-editor animation, connected-system animation, capability cards, logos and company information.

`README.md` alone contains the text, but its images require the accompanying `assets` folder. The animated GIFs are stored in your repository and use no external animation service.

Open `README-preview.html` in a browser to review the included layout locally. It is a GitHub-style preview; GitHub's final spacing and colors may differ. The preview, this setup guide and the generator are optional and do not need to be uploaded to your company repository.

## Where to use it

- **Company repository:** put `README.md` and `assets` in the repository root.
- **GitHub organization overview:** use an organization-owned `.github` repository. Put the README at `profile/README.md` and the supplied assets at `profile/assets/` so the relative paths still work.
- **Personal GitHub profile:** use a public repository whose name exactly matches your GitHub username. Put the README and assets at the root.

If you already have a project README with installation instructions, preserve those instructions and add the company sections around them. This package is a company introduction; it does not assume a software stack, release status or license.

## Software-focused redesign

- **Animated editor hero:** an eight-second code reveal, blinking cursor, changing software phrases and moving connection signals.
- **Connected-system animation:** a six-second sequence showing field devices, integration and a software interface, with moving packets and orbiting accents.
- **Responsive artwork:** portrait hero and connection layouts below a 600px viewport width; capability cards stack vertically on smaller screens.
- **Reduced motion:** `<picture>` sources select still artwork when the browser reports a reduced-motion preference. The still images are also linked explicitly in the README.
- **Developer-style presentation:** syntax colors, dark interface panels, monospaced details and blue/yellow company branding.
- **Company-grounded content:** digital monitoring, IoT integration, automation and building-system modernization, alongside both official websites.

The code editor and interface artwork are visual concepts. They do not define a software package, a live operating dashboard or the implementation language of your repositories.

## Visual assets

- `assets/alphanumeric-hero.gif` — desktop editor hero; `alphanumeric-hero-mobile.gif` is the portrait version.
- `assets/connected-software.gif` — desktop connection animation; `connected-software-mobile.gif` is the portrait version.
- Matching `.png` files — still alternatives for each animation.
- `assets/software-capabilities.png` and `software-capabilities-mobile.png` — desktop and stacked capability layouts.
- `assets/capability-*.png` — the four original capability cards.
- `assets/software-footer.png` — matching collaboration banner.
- `assets/brand-*.png` — official website logos placed on dark backgrounds.
- `assets/link-*.png` — clickable website and email labels.
- `assets/logo-*.png` — original logo files downloaded from the company websites.
- `assets/github-social-preview.png` — 1280 × 640 repository sharing image.

Text remains available outside the images. Both website links and the contact email are ordinary clickable links.

GitHub sanitizes README HTML, including scripts and inline styles. This README uses Markdown, supported basic HTML, `<picture>` elements and image files. The motion is embedded in GIF files.

## Optional: repository social preview

Open your GitHub repository, go to **Settings → General → Social preview → Edit → Upload an image**, and select `assets/github-social-preview.png`. This makes links to the repository carry the matching software-themed artwork.

## Optional: regenerate the assets

The original asset generator is included in `tools/generate_assets.py`. It requires Python 3, Pillow and the system fonts named in the script. Font fallbacks are provided; a different installed font may change the appearance slightly.

Run from the package root:

```bash
python -m pip install Pillow
python tools/generate_assets.py
```

No regeneration is required to use the supplied files.

## Content sources

Reviewed on **9 October 2026**:

- https://alphanumericinnovations.com/
- https://alphanumericinnovations.com/about.html
- https://alphanumericinnovations.com/contact.html
- https://alphanumericinnovations.com/iot_bms.html
- https://alphanumericet.com/
- https://alphanumericet.com/about.html
- https://alphanumericet.com/contact.html
- https://alphanumericet.com/bms-with-iot.html

Official logos:

- https://alphanumericinnovations.com/assets/img/lll.png
- https://alphanumericet.com/assets/logo-black.png

GitHub rendering references:

- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files
- https://github.com/github/markup
- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview

The website descriptions and contact details were checked against the live pages. No customer counts, certifications, performance figures, repository statistics or software compatibility claims were added.
