/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'

        './static/src/**/*.{js,jsx,ts,tsx}',
        
    ],
    theme: {
        extend: {
            colors:{
                'primary': '#5B21B6',
                'secondary': '#9333EA',
                'accent': '#FBBF24',
                'neutral': '#374151',
                'base-100': '#FFFFFF',
                'info': '#3ABFF8',
                'success': '#36D399',
                'warning': '#FBBD23',
                'error': '#F87272',
                'light': '#F9FAFB',
                'dark': '#111827',
                'muted': '#6B7280',
                'ultraViolet': '#726DA8',
                'glaucous': '#7D8CC4',
                'nonphotoBlue' : '#A0D2DB',
                'mintGreen' : '#BEE7E8',
                'englishViolet' : '#594157',
                'ultraViolet' : '#665780',
                brand:{
                    'platinum': '#ccdbdcff',
                    'non-photo-blue': '#9ad1d4ff',
                    'non-photo-blue-2': '#80ced7ff',
                    'cerulean': '#007ea7ff',
                    'prussian-blue': '#003249ff',
                }
                
                
            }
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        
    ],
}
