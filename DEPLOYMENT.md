# GitHub Pages Deployment Guide

This guide will help you deploy the Milano Real Estate Explorer to GitHub Pages.

## Prerequisites

- GitHub account
- Git installed on your computer
- Repository already initialized (done ✓)

## Step-by-Step Deployment

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Repository settings:
   - **Name**: `milano-real-estate-explorer` (or your preferred name)
   - **Description**: "Interactive visualization of Milan real estate OMI data"
   - **Public** (required for free GitHub Pages)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click "Create repository"

### 2. Connect Local Repository to GitHub

GitHub will show you commands. Use these:

```bash
cd "/Users/jacopo/Projects/Omi explorer"

# Add the remote repository (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/milano-real-estate-explorer.git

# Push the code
git branch -M main
git push -u origin main
```

### 3. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" (gear icon in the top menu)
3. In the left sidebar, click "Pages"
4. Under "Source":
   - Select "Deploy from a branch"
   - Branch: `main`
   - Folder: `/ (root)`
5. Click "Save"

### 4. Wait for Deployment

- GitHub will automatically build and deploy your site
- This usually takes 1-3 minutes
- You'll see a message like: "Your site is live at https://YOUR-USERNAME.github.io/milano-real-estate-explorer/"

### 5. Update README with Live URL

Once deployed, update the README.md:

```bash
# Edit README.md and replace the demo URL with your actual URL
# Then commit and push
git add README.md
git commit -m "Update live demo URL"
git push
```

## Custom Domain (Optional)

If you have a custom domain:

1. In the Pages settings, add your custom domain under "Custom domain"
2. Update your DNS records (see GitHub documentation)
3. Enable "Enforce HTTPS" after DNS propagates

## Updating the Site

After making changes:

```bash
# Make your changes to files
# Then commit and push
git add .
git commit -m "Description of changes"
git push

# GitHub Pages will automatically redeploy (takes 1-3 minutes)
```

## Rebuilding Data

If you update the OMI data:

```bash
# Place new CSV and KMZ files in the project folder
# Run the rebuild script
python3 rebuild.py

# Commit and push the updated index.html
git add index.html embedded_data.js zone_boundaries.js
git commit -m "Update OMI data to [new semester]"
git push
```

## Troubleshooting

### Site Not Loading
- Check that GitHub Pages is enabled in Settings → Pages
- Verify the branch is set to `main` and folder to `/ (root)`
- Wait a few minutes for deployment to complete

### 404 Error
- Make sure `index.html` is in the root directory
- Check that the file was pushed successfully: `git log --oneline`

### Map Not Displaying
- Check browser console for errors (F12 → Console)
- Verify all files are committed and pushed
- Clear browser cache and refresh

### Search Not Working
- This uses the Nominatim API which has rate limits
- If many people use the site simultaneously, some searches may be delayed
- The API is free and doesn't require an API key

## Performance Tips

1. **Large Files**: The HTML file is ~450KB due to embedded data
   - This is intentional for a self-contained application
   - GitHub Pages handles this fine
   - Consider CDN if traffic is very high

2. **Caching**: Browsers will cache the HTML after first load
   - Updates may require hard refresh (Ctrl+F5 or Cmd+Shift+R)

3. **Mobile**: The app is responsive but map interactions work best on desktop

## Security Notes

- All data is embedded in the HTML (no backend needed)
- Nominatim API is used for geocoding (free, public API)
- No user data is collected or stored
- No cookies or tracking

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Review GitHub Pages documentation
3. Open an issue in the repository
4. Check browser console for errors

---

**Your site will be live at:**
`https://YOUR-USERNAME.github.io/milano-real-estate-explorer/`

Remember to replace `YOUR-USERNAME` with your actual GitHub username!
