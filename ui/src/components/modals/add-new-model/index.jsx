import {
  RbitModal, SectionTitle, Steps,
} from '@radicalbit/radicalbit-design-system';
import useModals from '@Src/hooks/use-modals';
import { ModelTypeEnum } from '@Src/store/state/models/constants';
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
    case ModelTypeEnum.TEXT_GENERATION:
      return (<TextGenerationHeader />);

    default:
      return (
        <div className="flex flex-col gap-4">
          <SectionTitle title="New Model" />

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
          <div className="flex items-center justify-center basis-1/2">
            <div className="text-center">
              <strong>
                Select from the
                {' '}

                {variables.length}
              </strong>

              {' '}

              columns in
              <br />

              your schema the variables you are interested in
            </div>
          </div>

          <div className="flex items-center justify-center basis-1/2">
            <div className="text-center">
              <strong>Check</strong>

              {' '}

              that this section contains
              <br />

              <strong>features, target, predictions and timestamp</strong>
            </div>

          </div>
        </div>
      );

    case 3:
      return (
        <div className="flex justify-center">
          Identify ground truth (target), timestamp, prediction, and probability fields.
        </div>
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
