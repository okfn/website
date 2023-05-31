/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.{html,js}',
  ],
  theme: {
    extend: {
      borderWidth: {
        '3': '3px',
      },
      colors: {
        'okfn-blue': {
          DEFAULT: '#00d1ff', // pastel blue light
        },
        'okfn-green': {
          DEFAULT: '#adffed' // pastel green light
        },
        'okfn-purple': {
          DEFAULT: '#e077ff' // purple
        },
        'okfn-yellow': {
          DEFAULT: '#e4ff36' // yellow
        },
        'okfn-light-gray': {
          DEFAULT: '#f8f8f8' // light-gray
        },
        'okfn-link': {
          DEFAULT: '#00a9e0' // link
        },
        'okfn-content': {
          DEFAULT: '#e4ff36' // content
        },
      },
      dropShadow: {
        'okfn': '0 4px 4px rgba(0, 0, 0, 0.4)',
      },
      fontFamily: {
        'sans': '"HK Grotesk", sans-serif',
        'mono': '"Necto Mono", monospace',
        'display': '"HK Grotesk", sans-serif',
      },
      fontSize: {
        '2xs': '.6875rem',
        'h0': ['6.25rem', {
          lineHeight: '100%',
        }],
        'h1': ['3.4375rem', {
          lineHeight: '100%',
        }],
        'h2': ['2.5rem', {
          lineHeight: '100%',
        }],
        'h3': ['1.5rem', {
          lineHeight: '120%',
        }],
        'h4': ['1.25rem', {
          lineHeight: '120%',
        }],
        'h5': ['1rem', {
          lineHeight: '120%',
        }],
        'hl-h0': ['6.25rem', {
          lineHeight: '100%',
          fontFamily: '"Necto Mono", monospace',
        }],
        'hl-h1': ['3.4375rem', {
          lineHeight: '100%',
          fontFamily: '"Necto Mono", monospace',
        }],
        'hl-h2': ['2.5rem', {
          lineHeight: '100%',
          fontFamily: '"Necto Mono", monospace',
        }],
        'hl-h3': ['1.5rem', {
          lineHeight: '120%',
          fontFamily: '"Necto Mono", monospace',
        }],
        'hl-h4': ['1.25rem', {
          lineHeight: '120%',
          fontFamily: '"Necto Mono", monospace',
        }],
        'hl-h5': ['1rem', {
          lineHeight: '120%',
          fontFamily: '"Necto Mono", sans-serif',
        }],
        'okfn-lg': ['2.5rem', '120%'],
        'okfn-md': ['1.375rem', '140%'],
        'okfn-sm': ['1rem', '140%'],
      },
      gridTemplateColumns: {
        '14': 'repeat(14, minmax(0, 1fr))',
      },
      gridColumnEnd: {
        '14': '14',
        '15': '15',
      },
      spacing: {
        '3': '0.75rem',
        '24': '6rem',
      },
      screens: {
        '2lg': '1200px',
        'portrait': {'raw': '(orientation: portrait)'},
        'landscape': { 'raw': '(orientation: landscape)' },
        'max-sm': { 'max': '640px' },
        'max-md': { 'max': '767px' },
        'max-lg': { 'max': '1023px' },
        'max-2lg': { 'max': '1199px' },
        'max-xl': { 'max': '1279px' },
        'max-2xl': { 'max': '1535px' },
      },
    },
  },
  safelist: [
    {
      pattern: /^(bg|border|text)-okfn-(blue|green|purple|yellow|light-gray|link|content)(-[a-z]+)?$/,
      variants: ['md'],
    },
    {
      pattern: /^text-h([0-9]+)?$/,
      variants: ['md'],
    },
    {
      pattern: /^text-hl-h([0-9]+)?$/,
      variants: ['md'],
    },
    {
      pattern: /^text-okfn-(lg|md|sm)?$/,
      variants: ['md'],
    },
    {
      pattern: /^(bg|border|text)-(black|gray|white)(-[0-9]+)?$/,
      variants: ['md'],
    },
    {
      pattern: /^(w|h)-(full|screen|auto|16|20|30|40|52|60|72|80)/,
      variants: ['md'],
    },
  ],
  plugins: [],
}
