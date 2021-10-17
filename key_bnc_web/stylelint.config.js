module.exports = {
	extends: [
		'stylelint-config-standard',
		'stylelint-config-recommended-scss',
	],
	plugins: [
		'stylelint-scss',
	],
	// customSyntax: 'postcss-scss',
	customSyntax: ['postcss-scss'],
	rules: {
		indentation: 'tab',
		'selector-pseudo-element-no-unknown': [true, {
			ignorePseudoElements: ['v-deep'],
		}],
		'property-no-unknown': [true, {
			ignoreProperties: ['aspect-ratio'],
		}],
		'selector-class-pattern': [
			true,
			/[a-z][a-z_\-]*[a-z]/,
		],
	},
	ignoreFiles: [
		'dist/**/*',
		'coverage/**/*',
		'cypress/**/*',
	],
	overrides: [
		{
			files: '**/*.vue',
			customSyntax: 'postcss-html',
		},
	],
};
