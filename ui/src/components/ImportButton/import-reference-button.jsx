import { Button, Upload } from '@radicalbit/radicalbit-design-system';
import { modelsApiSlice } from '@State/models/api';
import ConfettiExplosion from 'react-confetti-explosion';
import { useParams } from 'react-router';

const { useImportReferenceDataMutation } = modelsApiSlice;

function ImportReferenceButton({ type = 'primary-light' }) {
  const { uuid: modelUUID } = useParams();

  const [triggerImportFeedback, { isLoading, isError }] = useImportReferenceDataMutation({ fixedCacheKey: `imports-reference-data-${modelUUID}` });
  const isSubmitDisabled = isLoading || isError;

  const disableUploadAction = () => false;

  const handleOnChange = async (info) => {
    const file = info?.file;
    await triggerImportFeedback({ file, modelUUID, successMessage: `Import ${file.name} file success` });
  };

  return (
    <div className="flex flex-row justfy-end w-full">

      <Upload
        accept=".csv"
        beforeUpload={disableUploadAction}
        disabled={isSubmitDisabled}
        fileList={[]}
        onChange={handleOnChange}
      >

        <Button disabled={isSubmitDisabled} loading={isLoading} onClick={() => {}} type={type}>Import Reference</Button>
      </Upload>

      <ConfettiExplosion
        duration={3000}
        force={0.9}
        particleCount={200}
        style={{ marginLeft: '-2rem' }}
        width={2000}
      />
    </div>
  );
}

export default ImportReferenceButton;
