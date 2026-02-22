import type { Config } from "stylelint";

export default {
	extends: [
		'stylelint-config-standard',
		'stylelint-config-recommended-scss',
	],
	plugins: [
		'stylelint-scss',
	],
	customSyntax: 'postcss-scss',
	rules: {
		'selector-pseudo-element-no-unknown': [true, {
			ignorePseudoElements: ['v-deep'],
		}],
		'property-no-unknown': [true, {
			ignoreProperties: ['aspect-ratio'],
		}],
		'selector-class-pattern': /[a-z][a-z_-]*[a-z]/,
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
} satisfies Config;
