import { GlobalWorkerOptions, getDocument } from 'pdfjs-dist';
import workerPath from 'pdfjs-dist/build/pdf.worker.js?url';
import { TextItem, TextMarkedContent } from 'pdfjs-dist/types/src/display/api';

// console.log(pdfjsLib);

GlobalWorkerOptions.workerSrc = workerPath;

export async function getPdfText(data: Uint8Array): Promise<string> {
	const pdfDocument = await getDocument(data).promise
	const promisedPages = new Array(pdfDocument.numPages)
		.fill(undefined)
		.map((_, idx) => idx + 1)
		.map((pageNumber) => pdfDocument
			.getPage(pageNumber)
			.then(page => page.getTextContent()))
	const pages = await Promise.allSettled(promisedPages)
	return pages
		.filter(isFulfilled)
		.flatMap(result => result.value.items.filter(isTextItem).map(({ str }) => str).join(''))
		.join('\n')
}

function isTextItem(_: TextItem | TextMarkedContent): _ is TextItem {
	return Boolean((_ as TextItem).str)
}

const isFulfilled = <T>(input: PromiseSettledResult<T>): input is PromiseFulfilledResult<T> =>
	input.status === 'fulfilled'
