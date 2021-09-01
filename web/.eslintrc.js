module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/essential',
    'eslint:recommended'
  ],
  parserOptions: {
    parser: 'babel-eslint'
  },
  rules: {
    'no-console': 'off',
    'no-debugger': 'off',
    'no-unneeded-ternary': 'off',
    'no-unused-vars': 'off',
    'no-tabs': 0,
    'indent': 'off',
    'comma-dangle': 'off',
    'eol-last': 'off',
    'no-mixed-spaces-and-tabs': 'off',
    'vue/no-unused-components': 'off',
    'no-multi-spaces': 'off',
    'Extra semicolon ': 'off',
    'no-unused-vars': 'off'
  },
  overrides: [
    {
      files: [
        '**/__tests__/*.{j,t}s?(x)',
        '**/tests/unit/**/*.spec.{j,t}s?(x)'
      ],
      env: {
        mocha: true
      }
    }
  ]
}
