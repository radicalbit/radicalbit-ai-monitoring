import {
  RbitModal, SectionTitle, Steps,
} from '@radicalbit/radicalbit-design-system';
import useModals from '@Src/hooks/use-modals';
import { ModelTypeEnum } from '@State/models/constants';
import ModalContextProvider, { useModalContext } from './modal-context-provider';
import ActionsStepFourth from './step-four/actions';
import BodyStepFour from './step-four/new-body';
import ActionsStepOne from './step-one/actions';
import BodyStepOne from './step-one/body';
import ActionsStepThree from './step-three/actions';
import BodyStepThree from './step-three/body';
import ActionsStepTwo from './step-two/actions';
import BodyStepTwo from './step-two/body';
import {
  TextGenerationActionButton, TextGenerationBody,
  TextGenerationHeader,
} from './text-generation';
import { EmbeddingsActionButton, EmbeddingsBody, EmbeddingsHeader } from './embeddings';

const { Step } = Steps;

function AddNewModel() {
  return (
    <ModalContextProvider>
      <AddNewModelInner />
    </ModalContextProvider>
  );
}

function AddNewModelInner() {
  const { setIsMaximize, isMaximize } = useModalContext();

  const { hideModal } = useModals();

  const handleOnMaximize = () => { setIsMaximize((b) => !b); };

  return (
    <RbitModal
      actions={(<Actions />)}
      header={<Header />}
      headerType="bold"
      isMaximize={isMaximize}
      maskClosable={false}
      maximizable
      onCancel={hideModal}
      onMaximize={handleOnMaximize}
      open
      scrollableBody
      width={1000}
    >
      <div className="flex flex-col gap-8">
        <Subtitles />

        <Body />
      </div>
    </RbitModal>
  );
}

function Header() {
  const {
    useFormbitStepOne,
    useFormbitStepTwo,
    useFormbitStepThree,
    useFormbitStepFour,
    step,
  } = useModalContext();

  const { isFormInvalid: isFormInvalidStepOne, form } = useFormbitStepOne;
  const modelType = form?.modelType;

  const { isFormInvalid: isFormInvalidStepTwo } = useFormbitStepTwo;
  const { isFormInvalid: isFormInvalidStepThree } = useFormbitStepThree;
  const { isFormInvalid: isFormInvalidStepFour } = useFormbitStepFour;

  const stepStatus = (step === 0 && isFormInvalidStepOne())
  || (step === 1 && isFormInvalidStepTwo())
  || (step === 2 && isFormInvalidStepThree())
  || (step === 3 && isFormInvalidStepFour()) ? 'error' : undefined;

  switch (modelType) {
    case ModelTypeEnum.EMBEDDINGS:
      return (<EmbeddingsHeader />);

    case ModelTypeEnum.TEXT_GENERATION:
      return (<TextGenerationHeader />);

    default:
      return (
        <div className="flex flex-col gap-4">
          <SectionTitle align="center" title="New Model" titleColor="primary" />

          <Steps className="w-3/4 self-center" current={step} direction="horizontal" status={stepStatus}>
            <Step title="Registry" />

            <Step title="Schema" />

            <Step title="Fields" />

            <Step title="Target" />
          </Steps>
        </div>
      );
  }
}

function Subtitles() {
  const { useFormbit, step } = useModalContext();
  const { form } = useFormbit;
  const variables = form?.variables ?? [];

  switch (step) {
    // step count start form 0
    case 1:
      return false;

    case 2:
      return (
        <div className="flex justify-between">
          <div className="basis-1/2">
            <SectionTitle
              align="center"
              size="small"
              title={(
                <p>
                  <strong>
                    Select from the
                    {' '}

                    {variables.length}
                  </strong>

                  {' '}

                  columns in
                  <br />

                  your schema the variables you are interested in
                </p>
              )}
              titleWeight="normal"
            />
          </div>

          <div className="basis-1/2">

            <SectionTitle
              align="center"
              modifier="basis-1/2"
              size="small"
              title={(
                <p>
                  <strong>Check</strong>

                  {' '}

                  that this section contains
                  <br />

                  <strong>features, target, predictions and timestamp</strong>
                </p>
              )}
              titleWeight="normal"
            />
          </div>

        </div>
      );

    case 3:
      return (
        <SectionTitle
          align="center"
          size="small"
          title={(
            <p>
              Identify ground truth (target), timestamp, prediction, and probability fields.
            </p>
        )}
          titleWeight="normal"
        />

      );

    default:
      return false;
  }
}

function Body() {
  const { useFormbitStepOne } = useModalContext();

  const { form } = useFormbitStepOne;
  const modelType = form?.modelType;

  switch (modelType) {
    case ModelTypeEnum.EMBEDDINGS:
      return <EmbeddingsBody />;

    case ModelTypeEnum.TEXT_GENERATION:
      return <TextGenerationBody />;

    default:
      return <BodyInner />;
  }
}

function BodyInner() {
  const { step } = useModalContext();

  switch (step) {
    // step count start form 0
    case 1:
      return <BodyStepTwo />;

    case 2:
      return <BodyStepThree />;

    case 3:
      return <BodyStepFour />;

    default:
      return <BodyStepOne />;
  }
}

function Actions() {
  const { useFormbitStepOne } = useModalContext();

  const { form } = useFormbitStepOne;
  const modelType = form?.modelType;

  switch (modelType) {
    case ModelTypeEnum.EMBEDDINGS:
      return (<EmbeddingsActionButton />);

    case ModelTypeEnum.TEXT_GENERATION:
      return (<TextGenerationActionButton />);

    default:
      return <ActionsInner />;
  }
}

function ActionsInner() {
  const { step } = useModalContext();

  switch (step) {
    // step count start form 0
    case 1:
      return <ActionsStepTwo />;

    case 2:
      return <ActionsStepThree />;

    case 3:
      return <ActionsStepFourth />;

    default:
      return <ActionsStepOne />;
  }
}

export default AddNewModel;
