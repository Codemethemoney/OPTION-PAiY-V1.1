module.exports = {
  root: true,
  extends: [
    '@react-native-community',
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:prettier/recommended',
    'plugin:@typescript-eslint/recommended', // 1. TypeScript Support
    'plugin:import/typescript',             // 3. Import Sorting (TypeScript) 
    'plugin:jsx-a11y/recommended', // 4. Accessibility
    'plugin:jest/recommended',    // 5. Jest Testing
    'plugin:react/jsx-runtime',
  ],
  parser: '@typescript-eslint/parser', // 1. TypeScript Support
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 2021,
    sourceType: 'module',
    project: './tsconfig.json',  // 1. TypeScript Support
  },
  plugins: [
    'react', 
    'react-native', 
    'prettier', 
    '@typescript-eslint', // 1. TypeScript Support
    'import',              // 3. Import Sorting
    'jsx-a11y',          // 4. Accessibility
    'jest'                 // 5. Jest Testing
  ],
  env: {
    'react-native/react-native': true,
    jest: true,
  },
  rules: {
    'react/prop-types': 'off',
    // ... your existing rules ...
    '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }], // 11. Unused Exports (TS)
    '@typescript-eslint/ban-ts-comment': 'off',
    'react/jsx-uses-react': 'off',
    'react/react-in-jsx-scope': 'off',
    'import/order': [ // 3. Import Sorting
      'warn',
      {
        'newlines-between': 'always',
        groups: [
          'builtin', 
          'external', 
          'internal', 
          'parent', 
          'sibling', 
          'index'
        ],
        pathGroups: [
          {
            pattern: '@/**',
            group: 'internal',
            position: 'after'
          }
        ],
        pathGroupsExcludedImportTypes: ['builtin'],
        alphabetize: { order: 'asc', caseInsensitive: true },
      },
    ],
    // 7. Naming Conventions (Example)
    '@typescript-eslint/naming-convention': [
      'warn',
      { 
        selector: 'default', 
        format: ['camelCase'] 
      },
      { 
        selector: 'typeLike', 
        format: ['PascalCase'] 
      },
      // ...add more naming conventions as needed
    ],
    // 12. Comment Style (Example)
    'spaced-comment': ['warn', 'always', {
      line: {
        markers: ['/'], 
        exceptions: ['-', '+']
      },
      block: {
        markers: ['!'],
        exceptions: ['*'],
        balanced: true
      }
    }],
  },
  settings: {
    react: {
      version: 'detect',
    },
    'import/resolver': {
      typescript: {}, // 3. Import Sorting (TypeScript)
    },
  },
  // 6. File Structure (Example)
  overrides: [
    {
      files: ['*.tsx'],
      rules: {
        // Add rules specific to .tsx files if needed
      }
    },
    {
      files: ['*.test.tsx'],
      rules: {
        // Add rules specific to test files if needed
      }
    }
  ]
};
