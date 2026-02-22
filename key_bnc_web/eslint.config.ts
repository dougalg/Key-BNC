import { defineConfig, globalIgnores } from "eslint/config";
import eslint from "@eslint/js";
import eslintPluginVue from "eslint-plugin-vue";
import typescriptEslint from "typescript-eslint";
import globals from "globals";

export default defineConfig([
	globalIgnores([
		"**/*.d.ts",
		"**/coverage",
		"**/dist",
		"key_bnc_wasm",
		"dist",
		"../pkg/**/*",
	]),
	{
		extends: [
			eslint.configs.recommended,
			...typescriptEslint.configs.recommended,
			...eslintPluginVue.configs["flat/recommended"],
		],
		files: ["**/*.{ts,vue}"],
		languageOptions: {
			ecmaVersion: "latest",
			sourceType: "module",
			globals: globals.browser,
			parserOptions: {
				parser: typescriptEslint.parser,
			},
		},
		rules: {
			"comma-dangle": [
				"error",
				{
					arrays: "always-multiline",
					objects: "always-multiline",
					imports: "always-multiline",
					exports: "always-multiline",
					functions: "always-multiline",
				},
			],
			"operator-linebreak": ["error", "before"],
			indent: ["error", "tab"],
			"no-tabs": ["error", { allowIndentationTabs: true }],
			"vue/html-indent": ["error", "tab"],
			"vue/multi-word-component-names": "off",
			"no-console":
				process.env.NODE_ENV === "production" ? "warn" : "off",
			"no-debugger":
				process.env.NODE_ENV === "production" ? "warn" : "off",
		},
	},
]);
