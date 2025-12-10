import {
  ErrorAlert, Header, Recap, UploadButton,
} from './form-fields';

function Csv() {
  return (
    <div className="flex justify-center mt-4">
      <div className="flex flex-col gap-4">

        <Header />

        <div className="flex flex-col gap-2">
          <UploadButton />

          <ErrorAlert />
        </div>

        <Recap />
      </div>
    </div>
  );
}

export default Csv;
