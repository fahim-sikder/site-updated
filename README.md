# Academic CV Website - Md Fahim Sikder

Personal academic CV website built with Hugo and HugoBlox (Academic CV theme).

**Live Site:** https://fahim-sikder.github.io/

## Technical Information

- **Hugo Version:** v0.152.2 (Extended)
- **Theme:** HugoBlox Academic CV (Tailwind)
- **Build Date:** Built with Hugo compiled on 2025-10-24
- **Deployment:** GitHub Pages

## Prerequisites

Before you begin, ensure you have installed:

- **Hugo Extended** (v0.152.0 or later) - [Installation Guide](https://gohugo.io/installation/)
- **Node.js and pnpm** (for asset processing)
- **Git** (for version control)

### Installing Hugo Extended

Download Hugo Extended from the [official releases page](https://github.com/gohugoio/hugo/releases). Make sure to download the **extended** version, as this site requires it for SCSS processing.

Verify your installation:
```bash
hugo version
# Should show: hugo v0.152.x-xxx+extended
```

## Getting Started

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/fahim-sikder/fahim-sikder.github.io.git
cd fahim-sikder.github.io

# Install dependencies
pnpm install

# Run the development server
hugo server
```

The site will be available at `http://localhost:1313/`

### Building for Production

```bash
# Build the site (output will be in /public directory)
hugo

# Build with drafts included
hugo --buildDrafts
```

## Site Structure

```
.
├── config/
│   └── _default/          # Configuration files
│       ├── hugo.yaml      # Main Hugo configuration
│       ├── params.yaml    # Site parameters
│       ├── menus.yaml     # Navigation menus
│       └── languages.yaml # Language settings
├── content/
│   ├── authors/           # Author profiles
│   ├── publications/      # Research publications
│   ├── project/           # Research projects
│   ├── blog/             # Blog posts
│   ├── post/             # Tutorial posts
│   ├── _index.md         # Homepage content
│   └── sections/         # Homepage sections
├── layouts/
│   ├── partials/         # Custom partial templates
│   │   └── project_publications.html  # Auto-links publications to projects
│   └── project/
│       └── single.html   # Custom project page layout
├── static/               # Static files (images, PDFs, etc.)
├── assets/              # Asset files (CSS, JS)
└── public/              # Generated site (git ignored)
```

## Creating New Content

### Adding a New Publication

```bash
hugo new publications/my-paper/index.md
```

Edit the frontmatter in `content/publications/my-paper/index.md`:

```yaml
---
title: "Your Paper Title"
date: 2024-01-01T00:00:00Z

# Authors (reference slugs from data/authors/*.yaml)
authors:
  - Md-Fahim-Sikder
  - Other-Author

# Publication type
publication_types: ["paper-conference"]

# Publication venue
publication: "*Conference Name 2024*"
publication_short: "CONF 2024"

# Abstract
abstract: >
  Your paper abstract here.

# Link to projects (will automatically show on project pages)
projects:
  - fairX
  - fair-decision-making

# Tags
tags:
  - Machine Learning
  - Fairness

# Links
links:
  - name: PDF
    url: "https://example.com/paper.pdf"
  - name: Code
    url: "https://github.com/username/repo"
  - name: Slides
    url: "uploads/slides.pdf"

# Featured image
image:
  filename: featured.jpg
  caption: "Figure caption"
  focal_point: Smart

featured: true
draft: false
---

Optional content here (details, additional information, etc.)
```

**Important:** Add the publication's featured image as `featured.jpg` in the same directory.

### Adding a New Project

```bash
hugo new project/my-project/index.md
```

Edit `content/project/my-project/index.md`:

```yaml
---
title: "Project Name"
date: 2024-01-01T00:00:00Z

# Summary for listing cards
summary: "Brief description of your project."

# Tags
tags:
  - Machine Learning
  - Python

# Featured image
image:
  filename: featured.jpg
  caption: "Project screenshot"
  focal_point: Smart

# Links
links:
  - name: Code
    url: https://github.com/username/repo
    icon: brands/github
  - name: Demo
    url: https://demo.example.com
    icon: globe

featured: true
draft: false
---

## About This Project

Detailed description of your project, methodology, results, etc.
```

**Note:** Publications with `projects: [my-project]` will **automatically appear** on this project's page thanks to the custom template implementation.

### Adding a Blog Post

```bash
hugo new blog/my-post/index.md
```

Edit `content/blog/my-post/index.md`:

```yaml
---
title: "Post Title"
date: 2024-01-01T00:00:00Z
summary: "Brief summary of the post"

# Featured image
image:
  filename: featured.jpg
  caption: "Image caption"

tags:
  - News
  - Updates

draft: false
---

Your blog post content in Markdown...
```

### Adding an Author Profile

Create a new file in `content/authors/new-author/_index.md`:

```yaml
---
title: New Author Name
role: PhD Student

# Social links
profiles:
  - icon: envelope
    url: mailto:author@example.com
  - icon: brands/github
    url: https://github.com/username
  - icon: brands/linkedin
    url: https://linkedin.com/in/username

# Organizations
organizations:
  - name: University Name
    url: https://university.edu
---

Author biography...
```

Add the author's avatar as `avatar.jpg` in the same directory.

## Custom Features

### Automatic Project-Publication Linking

This site includes a custom implementation that automatically displays publications on project pages:

1. **How it works:** Publications that include a project slug in their `projects:` field will automatically appear on that project's page.

2. **Implementation files:**
   - `layouts/partials/project_publications.html` - Queries and displays linked publications
   - `layouts/project/single.html` - Custom project layout that includes the publications section

3. **Usage:** Simply add the project slug to your publication's frontmatter:
   ```yaml
   projects:
     - fairX
     - fair-decision-making
   ```

No manual updates to project pages are needed—the linking happens automatically!

## Configuration

### Main Configuration Files

- **`config/_default/hugo.yaml`** - Core Hugo settings, site title, base URL
- **`config/_default/params.yaml`** - Site parameters, appearance, features
- **`config/_default/menus.yaml`** - Navigation menu configuration
- **`config/_default/languages.yaml`** - Language and localization settings

### Updating Site Information

Edit `config/_default/hugo.yaml`:
```yaml
title: Your Name
baseURL: 'https://your-site.com/'
```

## Common Tasks

### Preview Drafts

```bash
hugo server --buildDrafts
```

### Check for Broken Links

```bash
hugo --printPathWarnings
```

### Clear Cache

```bash
hugo --gc
rm -rf public/ resources/
```

### Update Theme

```bash
hugo mod get -u
hugo mod tidy
```

## Deployment

### GitHub Pages (Automatic)

This site is configured for automatic deployment via GitHub Actions. Push to the `main` branch to trigger a deployment.

### Manual Deployment

```bash
# Build the site
hugo --minify

# Deploy (contents of /public directory)
# Upload to your hosting provider or push to GitHub Pages
```

## Troubleshooting

### "Hugo command not found"
- Ensure Hugo Extended is installed and in your PATH
- Verify with `hugo version`

### "Port 1313 already in use"
- Stop other Hugo servers or use a different port:
  ```bash
  hugo server --port 1314
  ```

### Build Errors
- Clear cache: `hugo --gc && rm -rf public/ resources/`
- Check Hugo version: Must be v0.152.0+ Extended
- Verify all frontmatter YAML is valid

### Images Not Displaying
- Ensure images are in the correct directory (same as `index.md`)
- Check filename matches frontmatter (e.g., `featured.jpg`)
- Verify image formats are supported (JPG, PNG, WebP)

## Resources

- **Hugo Documentation:** https://gohugo.io/documentation/
- **HugoBlox Documentation:** https://docs.hugoblox.com/
- **Markdown Guide:** https://www.markdownguide.org/
- **Hugo Academic Theme Guide:** https://docs.ownable.dev/hugoblox/

## License

This site is based on the HugoBlox Academic CV theme.

Original theme: MIT © 2016-Present [George Cushen](https://georgecushen.com)

## Contact

For questions or issues, please contact Md Fahim Sikder or open an issue on the repository.
