import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { JOB_STATUS } from '@Src/constants';
import { Spinner, Void } from '@radicalbit/radicalbit-design-system';
import ImportCurrentDatasetButton from '@Components/ImportButton/import-current-button';
import ImportReferenceButton from '@Components/ImportButton/import-reference-button';
import { selectIsShowConfettiForModelCreation } from '@State/global-configuration/selectors';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';

function JobStatus({ jobStatus }) {
  const { uuid: modelUUID } = useParams();
  const isShowConfettiFroModel = useSelector((state) => selectIsShowConfettiForModelCreation(state, modelUUID));

  switch (jobStatus) {
    case JOB_STATUS.IMPORTING: {
      return (
        <Void
          description={(
            <>
              Data are being processed
              <br />
              As soon as they are available they will be displayed here
            </>
            )}
          image={<Spinner spinning />}
          modifier="h-full"
          title="Processing..."
        />
      );
    }

    case JOB_STATUS.ERROR: {
      return (
        <SomethingWentWrong />
      );
    }

    case JOB_STATUS.MISSING_REFERENCE: {
      return (
        <Void
          actions={(<ImportReferenceButton type="primary" />)}
          description={(
            <>
              Upload a CSV file to analyze and visualize the data.
              <br />
              This will allow you to see the outcome of your analysis.
            </>
          )}
          title={`Import a Reference File${isShowConfettiFroModel ? ' 🥳' : ''}`}
        />
      );
    }

    case JOB_STATUS.MISSING_CURRENT: {
      return (
        <Void
          actions={(<ImportCurrentDatasetButton type="primary" />)}
          description="Import a new dataset to see the outcome"
          title="No current dataset imported yet"
        />
      );
    }

    default: return false;
  }
}

export default JobStatus;
