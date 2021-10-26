module.exports = {
	root: true,
	env: {
		node: true,
	},
	extends: [
		'plugin:vue/vue3-recommended',
		'@vue/typescript/recommended',
	],
	parserOptions: {
		ecmaVersion: 2020,
	},
	rules: {
		'comma-dangle': ['error', {
			arrays: 'always-multiline',
			objects: 'always-multiline',
			imports: 'always-multiline',
			exports: 'always-multiline',
			functions: 'always-multiline',
		}],
		'operator-linebreak': ['error', 'before'],
		indent: ['error', 'tab'],
		'no-tabs': ['error', { allowIndentationTabs: true }],
		'vue/html-indent': ['error', 'tab'],
		'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
		'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
	},
	ignorePatterns: ['../pkg/**/*'],
}
