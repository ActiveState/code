[HttpPost]
public ActionResult Convert(FormCollection collection)
{
    // read parameters from the webpage
    string url = collection["TxtUrl"];

    string pdf_page_size = collection["DdlPageSize"];
    PdfPageSize pageSize = (PdfPageSize)Enum.Parse(typeof(PdfPageSize), pdf_page_size, true);

    string pdf_orientation = collection["DdlPageOrientation"];
    PdfPageOrientation pdfOrientation = (PdfPageOrientation)Enum.Parse(
        typeof(PdfPageOrientation), pdf_orientation, true);

    int webPageWidth = 1024;
    try
    {
        webPageWidth = System.Convert.ToInt32(collection["TxtWidth"]);
    }
    catch { }

    int webPageHeight = 0;
    try
    {
        webPageHeight = System.Convert.ToInt32(collection["TxtHeight"]);
    }
    catch { }

    // instantiate a html to pdf converter object
    HtmlToPdf converter = new HtmlToPdf();

    // set converter options
    converter.Options.PdfPageSize = pageSize;
    converter.Options.PdfPageOrientation = pdfOrientation;
    converter.Options.WebPageWidth = webPageWidth;
    converter.Options.WebPageHeight = webPageHeight;

    // create a new pdf document converting an url
    PdfDocument doc = converter.ConvertUrl(url);

    // save pdf document
    byte[] pdf = doc.Save();

    // close pdf document
    doc.Close();

    // return resulted pdf document
    FileResult fileResult = new FileContentResult(pdf, "application/pdf");
    fileResult.FileDownloadName = "Document.pdf";
    return fileResult;
}
