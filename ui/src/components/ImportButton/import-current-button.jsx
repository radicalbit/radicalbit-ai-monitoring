import { Button, Upload } from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router';

import { modelsApiSlice } from '@State/models/api';

const { useImportCurrentDataMutation } = modelsApiSlice;

function ImportCurrentDatasetButton({ type = 'primary-light' }) {
  const { uuid: modelUUID } = useParams();

  const [triggerImportFeedback, { isLoading, isError }] = useImportCurrentDataMutation({ fixedCacheKey: `imports-reference-data-${modelUUID}` });
  const isSubmitDisabled = isLoading || isError;

  const disableUploadAction = () => false;

  const handleOnChange = async (info) => {
    const file = info?.file;
    await triggerImportFeedback({ file, modelUUID, successMessage: `Import ${file.name} file success` });
  };

  return (
    <Upload
      accept=".csv"
      beforeUpload={disableUploadAction}
      disabled={isSubmitDisabled}
      fileList={[]}
      onChange={handleOnChange}
    >
      <Button disabled={isSubmitDisabled} loading={isLoading} type={type}>Import Current</Button>
    </Upload>
  );
}

export default ImportCurrentDatasetButton;
