<template>
	<div>
		<h2>Manage Corpus</h2>
		<form ref="form">
			<input
				id="fileinput"
				ref="input"
				type="file"
				class="file-input"
				multiple
				@change="onFileChange"
			>
			<label
				for="fileinput"
				class="no-outline"
			>
				Add files
			</label>
		</form>
		<p>{{ allFiles.length }} files loaded.</p>
		<ul class="file-list">
			<li
				v-for="f in allFiles"
				:key="f.id"
				class="file-list-item"
			>
				<span>{{ f.name }}</span>
				<basic-button @click="removeFile(f.id)">
					Remove
				</basic-button>
			</li>
		</ul>
	</div>
</template>

<script lang="ts">
import { defineComponent, PropType, reactive, Ref, ref, toRefs } from '@vue/runtime-core'
import { KeyBnc } from 'key_bnc_wasm'
import { PdfToText } from 'pdf_text_wasm';
import BasicButton from './buttons/BasicButton.vue'

interface FileObject {
	name: string;
	id: number;
}

export default defineComponent({
	components: { BasicButton },
	props: {
		keyBnc: {
			type: Object as PropType<KeyBnc>,
			required: true,
		},
	},
	emits: ['corpus-changed'],
	setup (props, ctx) {
		const form: Ref<HTMLFormElement | null> = ref(null)
		const input: Ref<HTMLInputElement | null> = ref(null)
		const state = reactive({
			allFiles: [] as FileObject[],
		})

		const processFile = (f: File) => {
			const name = f.name
			if (f.type.toLocaleLowerCase() === 'application/pdf') {
				const fileReader = new FileReader()
				fileReader.onloadend = (event: ProgressEvent<FileReader>) => {
					if (!event.target) {
						return;
					}
					const result = PdfToText.new().read_file(new Uint8Array(event.target.result as ArrayBuffer));
					console.log(result);
				}
				fileReader.readAsArrayBuffer(f)
			} else {
				const fileReader = new FileReader()
				fileReader.onloadend = () => {
					const id = props.keyBnc.add_entry(fileReader)
					state.allFiles.push({
						id,
						name,
					})
				}
				fileReader.readAsText(f)
				ctx.emit('corpus-changed')
			}
		}

		const onFileChange = () => {
			if (!input.value || input.value.files === null) {
				return
			}

			for (let i = 0; i < input.value.files.length; i++) {
				const f = input.value.files[i]
				if (f !== null) {
					processFile(f)
				}
			}

			if (form.value) {
				form.value.reset()
			}
		}

		const removeFile = (toRemove: number) => {
			props.keyBnc.remove_entry(toRemove)
			state.allFiles = [...state.allFiles.filter(({ id }) => id !== toRemove)]
			ctx.emit('corpus-changed')
		}

		return {
			...toRefs(state),
			form,
			input,
			removeFile,
			onFileChange,
		}
	},
})
</script>

<style lang="scss" scoped>
.file-list {
	> * + * {
		margin-top: 1rem;
	}
}

.file-list-item {
	> * + * {
		margin-left: 1rem;
	}
}

[type="file"] {
	border: 0;
	clip: rect(0, 0, 0, 0);
	height: 1px;
	overflow: hidden;
	padding: 0;
	position: absolute !important;
	white-space: nowrap;
	width: 1px;
}

[type="file"] + label {
	background-color: #000;
	border-radius: 5px;
	color: #fff;
	cursor: pointer;
	display: inline-block;
	font-family: Poppins, sans-serif;
	font-size: 1rem;
	font-weight: 700;
	height: 4rem;
	line-height: 4rem;
	padding-left: 2rem;
	padding-right: 2rem;
	transition: background-color 0.3s;
	border: 2px solid black;
}

[type="file"]:focus + label,
[type="file"] + label:hover {
	background-color: white;
	color: black;
}

[type="file"]:focus + label {
	outline: 1px dotted #000;
	outline: -webkit-focus-ring-color auto 5px;
}
</style>
