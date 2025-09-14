Write-Host "🔧 Setting up TailwindCSS config manually..."

# --- tailwind.config.js ---
$tailwindConfig = @(
  "/** @type {import('tailwindcss').Config} */",
  "module.exports = {",
  "  content: [",
  "    './index.html',",
  "    './src/**/*.{vue,js,ts,jsx,tsx}'",
  "  ],",
  "  theme: {",
  "    extend: {},",
  "  },",
  "  plugins: [],",
  "}"
)
$tailwindConfig | Set-Content -Encoding UTF8 "tailwind.config.js"
Write-Host "✅ Created tailwind.config.js"

# --- postcss.config.js ---
$postcssConfig = @(
  "module.exports = {",
  "  plugins: {",
  "    tailwindcss: {},",
  "    autoprefixer: {},",
  "  },",
  "}"
)
$postcssConfig | Set-Content -Encoding UTF8 "postcss.config.js"
Write-Host "✅ Created postcss.config.js"

# --- src/assets/tailwind.css ---
New-Item -ItemType Directory -Force -Path "src/assets" | Out-Null
$tailwindCSS = @(
  "@tailwind base;",
  "@tailwind components;",
  "@tailwind utilities;"
)
$tailwindCSS | Set-Content -Encoding UTF8 "src/assets/tailwind.css"
Write-Host "✅ Created src/assets/tailwind.css"

# --- Inject import into main.js ---
$mainFile = "src/main.js"
$importLine = "import './assets/tailwind.css'"

if (Test-Path $mainFile) {
    $content = Get-Content $mainFile
    if ($content -notcontains $importLine) {
        $importLine | Set-Content -Path temp-main.js
        $content | Add-Content -Path temp-main.js
        Move-Item -Force temp-main.js $mainFile
        Write-Host "✅ Added Tailwind import to $mainFile"
    }
    else {
        Write-Host "ℹ️ Tailwind import already exists in $mainFile"
    }
}
else {
    Write-Host "⚠️ $mainFile not found. Please check your project structure."
}

Write-Host "🎉 TailwindCSS setup completed!"
