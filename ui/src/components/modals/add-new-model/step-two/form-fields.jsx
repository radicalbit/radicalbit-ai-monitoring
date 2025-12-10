import { faTriangleExclamation, faUpload } from '@fortawesome/free-solid-svg-icons';
import {
  AlertLegacy,
  Button,
  FontAwesomeIcon,
  SectionTitle,
  Upload,
} from '@radicalbit/radicalbit-design-system';
import { useModalContext } from '../modal-context-provider';
import useHandleOnNext from './use-handle-on-next';

function Header() {
  return (
    <SectionTitle
      subtitle={(
        <p>
          Upload your CSV file containing a representative sample of the data you want to monitor.

          <br />

          The uploaded file will be used to automatically infer variables names, data types,
          <br />
          and construct the corresponding schema
        </p>
      )}
      titleWeight="normal"
    />
  );
}

function UploadButton() {
  const { args } = useHandleOnNext();

  const { useFormbit } = useModalContext();
  const {
    form, setError, remove, writeAll,
  } = useFormbit;

  const fileList = form.file ? [form.file] : undefined;

  const beforeUpload = (file) => {
    const isTooBig = file.size / 1024 > 2000;

    if (isTooBig) {
      setError('file', 'File must be smaller than 2MB');
    }

    return !isTooBig;
  };

  const handleOnChange = async ({ fileList: currList, file: { originFileObj } }) => {
    if (currList.length) {
      writeAll([
        [
          'file',
          originFileObj,
          {
            pathsToValidate: ['file'],
          },
        ],
        ['__metadata.clearFieldNextStep', true],
      ]);
    }
  };

  const handleOnRemove = () => {
    remove('file');
    setError('file', undefined);
    setError('silent.backend', undefined);
  };

  return (
    <div className="w-2/5">
      <Upload
        accept=".csv"
        beforeUpload={beforeUpload}
        behavior="hide-button"
        customRequest={() => {}}
        fileList={fileList}
        onChange={handleOnChange}
        onRemove={handleOnRemove}
      >
        <Button
          disabled={args.isLoading}
          prefix={<FontAwesomeIcon icon={faUpload} />}
          type="primary"
        >
          Upload CSV
        </Button>
      </Upload>
    </div>
  );
}

function Recap() {
  return (
    <div>
      <SectionTitle size="small" title="Date File Specifications:" />

      <ul>
        <li>
          <label>
            <strong>Header Row: </strong>
            Define variable names (column headers) in the first row
          </label>
        </li>

        <li>
          <label>
            <strong>Trailing Newline: </strong>
            Optional (newline character at file end)
          </label>
        </li>

        <li>
          <label>
            <strong>Field Delimiters: </strong>

            Double quotes (") or unquoted (consistent throughout)
          </label>
        </li>

        <li>
          <label>
            <strong>Line Breaks: </strong>
            Not supported within fields
          </label>
        </li>

        <li>
          <label>
            <strong>File Size Limit: </strong>
            2MB ( if your file is bigger please use our SDK )
          </label>
        </li>
      </ul>
    </div>
  );
}

function ErrorAlert() {
  const { useFormbit } = useModalContext();
  const { error } = useFormbit;

  if (error('file') || error('silent.backend')) {
    const errorsList = (error('file') || error('silent.backend')).split('\n').map((e, index) => <li key={index}>{e}</li>);

    return (
      <AlertLegacy
        icon={<FontAwesomeIcon icon={faTriangleExclamation} />}
        text={(
          <>
            <strong>The file is not compliant, we found this problems to solve:</strong>

            <ul className="no-margin-bottom">
              {errorsList}
            </ul>
          </>
            )}
        type="error"
      />
    );
  }

  return false;
}

export {
  ErrorAlert,
  Header,
  Recap,
  UploadButton,
};
