const path = require('path');

const off = 'off';
const warn = 'warn';
const error = 'error';

const listOfRules = {
  a11y: {
    'jsx-a11y/anchor-is-valid': [warn, { aspects: ['invalidHref'] }],
    'jsx-a11y/click-events-have-key-events': off,
    'jsx-a11y/control-has-associated-label': off,
    'jsx-a11y/label-has-associated-control': off,
    'jsx-a11y/label-has-for': off,
    'jsx-a11y/no-autofocus': off,
    'jsx-a11y/no-static-element-interactions': off,
  },
  import: {
    'import/extensions': [error],
    'import/no-cycle': off,
    'import/no-named-as-default': off,
    'import/no-unresolved': [error],
    'import/prefer-default-export': off,
  },
  misc: {
    'comma-dangle': [error, 'always-multiline'],
    'max-len': off,
    'no-confusing-arrow': off,
    'no-console': off,
    'no-nested-ternary': off,
    'no-param-reassign': [error, { ignorePropertyModificationsFor: ['draft'], props: true }],
    'no-shadow': warn,
    'no-use-before-define': off,
    'no-underscore-dangle': off,
    camelcase: [error],
  },
  react: {
    'react-hooks/exhaustive-deps': warn,
    'react-hooks/rules-of-hooks': error,
    'react/destructuring-assignment': off,
    'react/forbid-prop-types': off,
    'react/jsx-filename-extension': off,
    'react/jsx-newline': [error, { prevent: false }],
    'react/jsx-no-duplicate-props': [error, { ignoreCase: false }],
    'react/jsx-no-useless-fragment': error,
    'react/jsx-props-no-spreading': off,
    'react/no-access-state-in-setstate': off,
    'react/no-array-index-key': off,
    'react/prop-types': off,
    'react/require-default-props': off,
    'react/state-in-constructor': off,
    'react/static-property-placement': off,
    'react/react-in-jsx-scope': off,
    'react/jsx-sort-props': [error, {
      callbacksLast: false,
      shorthandFirst: false,
      shorthandLast: false,
      ignoreCase: true,
      noSortAlphabetically: false,
      reservedFirst: ['key'],
    }],
    'no-param-reassign': ['error', { props: true, ignorePropertyModificationsFor: ['state', 'draft'] }],
    'react/no-unstable-nested-components':[off]
  },
};

const rules = {
  ...listOfRules.import,
  ...listOfRules.a11y,
  ...listOfRules.misc,
  ...listOfRules.react,
};

module.exports = {
  root: true,
  extends: [
    'airbnb',
    'eslint:recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parserOptions: {
    ecmaVersion: 11,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  plugins: [
    'jsx-a11y',
    'react',
    'react-hooks',
  ],

  rules,

  settings: {
    'import/resolver': {
      alias: {
        map: [
          ['@Api', path.resolve(__dirname, './src/api')],
          ['@Components', path.resolve(__dirname, './src/components')],
          ['@Container', path.resolve(__dirname, './src/container')],
          ['@Helpers', path.resolve(__dirname, './src/helpers')],
          ['@Hooks', path.resolve(__dirname, './src/hooks')],
          ['@Img', path.resolve(__dirname, './src/resources/images')],
          ['@Modals', path.resolve(__dirname, './src/components/modals')],
          ['@Src', path.resolve(__dirname, './src')],
          ['@State', path.resolve(__dirname, './src/store/state')],
          ['@Store', path.resolve(__dirname, './src/store')],
          ['@Styles', path.resolve(__dirname, './src/styles')],
        ],
        extensions: ['.js', '.jsx', '.json'],
      },
    },
    'import/extensions': [{ ignorePackages: true }],
  },
}

