type AsyncFileReader = (f: File) => Promise<ProgressEvent<FileReader>>;

export const readFileAsText = createAsyncFileReader('readAsText');

export const readFileAsArrayBuffer = createAsyncFileReader('readAsArrayBuffer');

function createAsyncFileReader(method: 'readAsArrayBuffer' | 'readAsText'): AsyncFileReader {
	return (f: File) => {
		const fileReader = new FileReader();
		return new Promise((resolve, reject) => {
			fileReader[method](f)
			fileReader.onloadend = (e: ProgressEvent<FileReader>) => resolve(e)
			fileReader.onerror = (e: ProgressEvent<FileReader>) => reject(e)
		});
	}
}

interface TargettedFileReaderProgressEvent extends ProgressEvent<FileReader> {
	target: FileReader;
}

export function validateEventTarget(event: ProgressEvent<FileReader>): asserts event is TargettedFileReaderProgressEvent {
	if (!event.target) {
		throw new Error(`Error reading file: ${JSON.stringify(event)}`)
	}
}
