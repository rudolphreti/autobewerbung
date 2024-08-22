function extractJobInformationUsingXPath() {
    // Base XPath for the job list
    const baseXPath = '/html/body/div[1]/div[3]/div/div[4]/div/div[1]/div[1]/div[1]/div[6]/ol';

    const jobList = document.evaluate(baseXPath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    
    // Regular expression for cleaning job positions
    const regexToRemove = /\(mwd\)|\(w\/m\/d\)|m\/w\/d|\(m\/w\/d\)|\/in|:in|\(f\/m\/d\)|\(w\/m\/\*\)|\(m\/f\/x\)|\(M\/W\)|\(m\/w\/d\)|\(all genders\)|\(w\/m\/x\)|\(m\/f\/d\)|\(d\/w\/m\)/gi;

    let allJobData = '';

    if (jobList) {
        const numberOfJobs = jobList.children.length;
        for (let i = 1; i <= numberOfJobs; i++) {
            // XPath for the job link and position (now correctly fetching text node)
            const xpathForLink = `${baseXPath}/li[${i}]/div/div/div[2]/h2/a`;
            const linkElement = document.evaluate(xpathForLink, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            const jobPosition = linkElement ? document.evaluate('text()', linkElement, null, XPathResult.STRING_TYPE, null).stringValue.trim() : '';

            // Updated XPath for the company using <a> tag
            const xpathForCompany = `${baseXPath}/li[${i}]/div/div/div[2]/div[2]/a`;
            const companyElement = document.evaluate(xpathForCompany, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            const companyName = companyElement ? companyElement.textContent.trim() : '';

            // Clean up the job position text
            const cleanPosition = jobPosition.replace(regexToRemove, '');

            const jobInfo = JSON.stringify({
                URL: linkElement ? linkElement.href : '',
                position: cleanPosition,
                company: companyName
            });

            allJobData += (i === 1 ? '' : ',') + jobInfo; // Add comma before each object except the first
        }
    }

    return allJobData;
}

// Call the function and log the result
const jobDataJSON = extractJobInformationUsingXPath();
console.log(jobDataJSON);
