import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { JOB_STATUS } from '@Src/constants';
import { Spinner, Void } from '@radicalbit/radicalbit-design-system';
// @ts-ignore
import LogoSquared from '@Img/logo-collapsed.svg';
import ImportReferenceButton from '@Components/ImportButton/import-reference-button';
import ImportCurrentDatasetButton from '@Components/ImportButton/import-current-button';

function JobStatus({ jobStatus }) {
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
          description="Import a reference file to see the outcome"
          image={<LogoSquared />}
          title="No reference data imported yet"
        />
      );
    }

    case JOB_STATUS.MISSING_CURRENT: {
      return (
        <Void
          actions={(<ImportCurrentDatasetButton type="primary" />)}
          description="Import a new dataset to see the outcome"
          image={<LogoSquared />}
          title="No current dataset imported yet"
        />
      );
    }

    default: return false;
  }
}

export default JobStatus;
