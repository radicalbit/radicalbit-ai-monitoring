import { DataTypeEnum, ModelTypeEnum } from '@State/models/constants';
import useFormbit from '@radicalbit/formbit';
import {
  createContext,
  useContext,
  useMemo,
  useState,
} from 'react';
import schemaStepFour from './step-four/schema';
import schemaStepOne from './step-one/schema';
import schemaStepThree from './step-three/schema';
import schemaStepTwo from './step-two/schema';

const modalContext = createContext(undefined);

function ModalContextProvider({ children }) {
  const [step, setStep] = useState(0);
  const [isMaximize, setIsMaximize] = useState(false);

  const useFormbitStepOne = useFormbit({
    initialValues: { modelType: ModelTypeEnum.BINARY_CLASSIFICATION, dataType: DataTypeEnum.TABULAR },
    yup: schemaStepOne,
  });

  const useFormbitStepTwo = useFormbit({
    initialValues: { separator: ',', __metadata: { clearFieldNextStep: true } },
    yup: schemaStepTwo,
  });

  const useFormbitStepThree = useFormbit({
    initialValues: { __metadata: { clearFieldNextStep: true } },
    yup: schemaStepThree,
  });

  const useFormbitStepFour = useFormbit({
    initialValues: {},
    yup: schemaStepFour,
  });

  const value = useMemo(() => {
    switch (step) {
      case 0: {
        return {
          isMaximize,
          setIsMaximize,
          step,
          setStep,
          useFormbit: useFormbitStepOne,
          useFormbitStepOne,
          useFormbitStepTwo,
          useFormbitStepThree,
          useFormbitStepFour,
        };
      }

      case 1: {
        return {
          isMaximize,
          setIsMaximize,
          step,
          setStep,
          useFormbit: useFormbitStepTwo,
          useFormbitStepOne,
          useFormbitStepTwo,
          useFormbitStepThree,
          useFormbitStepFour,
        };
      }

      case 2: {
        return {
          isMaximize,
          setIsMaximize,
          step,
          setStep,
          useFormbit: useFormbitStepThree,
          useFormbitStepOne,
          useFormbitStepTwo,
          useFormbitStepThree,
          useFormbitStepFour,
        };
      }

      default: {
        return {
          isMaximize,
          setIsMaximize,
          step,
          setStep,
          useFormbit: useFormbitStepFour,
          useFormbitStepOne,
          useFormbitStepTwo,
          useFormbitStepThree,
          useFormbitStepFour,
        }; }
    }
  }, [isMaximize, step, useFormbitStepFour, useFormbitStepOne, useFormbitStepThree, useFormbitStepTwo]);

  return (
    <modalContext.Provider value={value}>
      {children}
    </modalContext.Provider>
  );
}

export const useModalContext = () => useContext(modalContext);
export default ModalContextProvider;
