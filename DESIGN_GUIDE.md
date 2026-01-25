# design guide & template

this document outlines the design principles, color palette, and component patterns for the merc1305 lab project. all sub-pages should follow these guidelines to maintain a unified visual identity.

## design philosophy
- **glassmorphism**: use translucent backgrounds with blur effects for cards and interactive elements.
- **high contrast**: bright cyan and purple accents on a deep black background.
- **vibrant backgrounds**: subtle radial gradients and animated blobs to provide depth without distractions.
- **automation focus**: engineering-grade clarity with professional terminology.

## design tokens (css variables)
all styles are centralized in `index.css`. use these variables:
- `--bg-color`: `#050505` (deep black)
- `--accent-color`: `#00f2ff` (cyan)
- `--accent-secondary`: `#7000ff` (purple)
- `--text-primary`: `#ffffff` (white)
- `--text-secondary`: `#a0a0a0` (gray)
- `--glass-bg`: `rgba(255, 255, 255, 0.03)`
- `--glass-border`: `rgba(255, 255, 255, 0.1)`

## core components

### 1. background structure
every page should include the background elements:
```html
<div class="bg-gradient"></div>
<div class="bg-blobs">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
</div>
```

### 2. "back to lab" navigation
use the standard `.back-link` class with the specific svg arrow:
```html
<a href="../index.html" class="back-link">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"></line>
        <polyline points="12 19 5 12 12 5"></polyline>
    </svg>
    back to lab
</a>
```

### 3. glass cards
use `.glass-card` for content sections:
```html
<div class="glass-card">
    <h2>section title</h2>
    <p>content goes here...</p>
</div>
```

## page template
use this boilerplate for new lab tools or articles:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>page title | merc1305 lab</title>
    
    <!-- fonts & global styles -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../index.css">
    
    <!-- page specific styles -->
    <style>
        .page-content { margin-top: 4rem; }
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    <div class="bg-blobs"><div class="blob blob-1"></div><div class="blob blob-2"></div></div>

    <main class="container page-content">
        <a href="../index.html" class="back-link">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            back to lab
        </a>

        <header>
            <span class="badge">category</span>
            <h1>page header</h1>
            <p>description or subheader</p>
        </header>

        <section>
            <div class="glass-card">
                <h2>content area</h2>
                <p>implementation goes here.</p>
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 merc1305. exploring the boundaries of technology.</p>
        </div>
    </footer>
</body>
</html>
```
