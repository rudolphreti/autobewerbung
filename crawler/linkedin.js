function extractJobInformationUsingXPath() {
  const baseXPath =
    '/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul';
  const jobList = document.evaluate(
    baseXPath,
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
  ).singleNodeValue;

  // Regular expression to remove unwanted characters
  const regexToRemove =
    /\(mwd\)|\(w\/m\/d\)|m\/w\/d|\(m\/w\/d\)|\/in|:in|\(f\/m\/d\)|\(w\/m\/\*\)|\(m\/f\/x\)|\(M\/W\)|\(m\/w\/d\)|\(all genders\)|\(w\/m\/x\)|\(m\/f\/d\)|\(d\/w\/m\)/gi;

  let allJobData = '';

  if (jobList) {
    const numberOfJobs = jobList.children.length;
    for (let i = 1; i <= numberOfJobs; i++) {
      const xpathForLink = `${baseXPath}/li[${i}]/div/div/div[1]/div/div[2]/div[1]/a`;
      const linkElement = document.evaluate(
        xpathForLink,
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
      ).singleNodeValue;
      const positionElement = linkElement
        ? linkElement.querySelector('span strong')
        : null;

      const xpathForCompany = `${baseXPath}/li[${i}]/div/div/div[1]/div/div[2]/div[2]/span`;
      const companyElement = document.evaluate(
        xpathForCompany,
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
      ).singleNodeValue;

      const jobUrl = linkElement ? linkElement.href : '';
      let jobPosition = positionElement
        ? positionElement.textContent.trim()
        : '';
      const companyName = companyElement
        ? companyElement.textContent.trim()
        : '';

      // Clean up job position text
      jobPosition = jobPosition.replace(regexToRemove, '');

      const jobInfo = JSON.stringify({
        URL: jobUrl,
        position: jobPosition,
        company: companyName,
      });

      allJobData += (i === 1 ? '' : ',') + jobInfo; // Add comma before each object except the first
    }
  }

  return allJobData;
}

// Call the function and log the result
const jobDataJSON = extractJobInformationUsingXPath();
console.log(jobDataJSON);
