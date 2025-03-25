import { Button, Upload } from '@radicalbit/radicalbit-design-system';
import { selectIsShowConfettiForModelCreation } from '@State/global-configuration/selectors';
import { globalConfigSliceActions } from '@State/global-configuration/slice';
import { modelsApiSlice } from '@State/models/api';
import ConfettiExplosion from 'react-confetti-explosion';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';

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
    <div className="flex flex-col justfy-end w-full">

      <Upload
        accept=".csv"
        beforeUpload={disableUploadAction}
        disabled={isSubmitDisabled}
        fileList={[]}
        onChange={handleOnChange}
      >
        <Button disabled={isSubmitDisabled} loading={isLoading} onClick={() => {}} type={type}>Import Reference</Button>
      </Upload>

      <ConfettiOS />

    </div>
  );
}

function ConfettiOS() {
  const { uuid: modelUUID } = useParams();
  const dispatch = useDispatch();

  const isShowConfettiForModel = useSelector((state) => selectIsShowConfettiForModelCreation(state, modelUUID));

  const handleOnComplete = () => {
    dispatch(globalConfigSliceActions.removeModelFromShowConfettiList(modelUUID));
  };

  if (isShowConfettiForModel) {
    return (
      <ConfettiExplosion
        duration={3000}
        force={0.9}
        onComplete={handleOnComplete}
        particleCount={200}
        style={{ marginLeft: '5rem' }}
        width={2000}
      />
    );
  }

  return false;
}

export default ImportReferenceButton;
