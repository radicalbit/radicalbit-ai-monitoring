import { faTriangleExclamation, faUpload } from '@fortawesome/free-solid-svg-icons';
import {
  AlertLegacy,
  Button,
  FontAwesomeIcon,
  FormField,
  Radio,
  SectionTitle,
  Upload,
} from '@radicalbit/radicalbit-design-system';
import useHandleOnNext from './use-handle-on-next';
import { useModalContext } from '../modal-context-provider';

const RadioGroup = Radio.Group;

function Header() {
  return (
    <SectionTitle
      subtitle={(
        <>
          Upload your CSV file containing a representative sample of the data you want to monitor.

          <br />

          The uploaded file will be used to automatically infer variables names, data types,
          <br />
          and construct the corresponding schema
        </>
      )}
      title="Upload CSV file"
      titleWeight="normal"
    />
  );
}

function Seperator() {
  const { useFormbit } = useModalContext();
  const { form, error, writeAll } = useFormbit;

  const handleOnChangeSeparator = ({ target: { value } }) => {
    writeAll([
      ['separator', value],
      ['__metadata.clearFieldNextStep', true],
    ]);
  };

  return (
    <FormField message={error('separator')}>
      <div className="flex flex-col">
        <SectionTitle size="small" title="CSV Separator:" />

        <RadioGroup modifier="margin-05" onChange={handleOnChangeSeparator} value={form.separator}>
          <Radio id="separator-comma" value=",">
            <label className="cursor-pointer" htmlFor="separator-comma">Comma (,)</label>
          </Radio>

          <Radio id="separator-semicolon" value=";">
            <label className="cursor-pointer" htmlFor="separator-semicolon">Semicolon (;)</label>
          </Radio>
        </RadioGroup>
      </div>
    </FormField>
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
    const isTooBig = file.size / 1024 > 500;

    if (isTooBig) {
      setError('file', 'File must be smaller than 500KB');
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
        fileList={fileList}
        onChange={handleOnChange}
        onRemove={handleOnRemove}
      >
        <Button
          disabled={args.isLoading}
          prefix={<FontAwesomeIcon icon={faUpload} />}
          type="primary"
        >
          Import CSV
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
            500KB max
          </label>
        </li>

        <li>
          <label>
            <strong>Data Row Limit: </strong>
            100 rows max
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
  Seperator,
  UploadButton,
};
