// Verify keyword injection theory for 7 services and 10 niches
const fs = require('fs');

const SERVICE_KEYWORDS = {
  'pseo-engine': [
    'sitemap', 'canonical', 'robots', 'crawler', 'indexing', 'indexnow', 'metadata', 'schema',
    'microdata', 'breadcrumbs', 'richresults', 'serp', 'rankings', 'organic', 'keywords', 'longtail',
    'searchconsole', 'crawlbudget', 'slugs', 'permalinks', 'backlinks', 'domainauthority', 'pagetag',
    'corewebvitals', 'cls', 'lcp', 'fid', 'inp', 'ttfb', 'prerender', 'ssr', 'ssg', 'isr',
    'revalidation', 'edgecache', 'cdn', 'cloudflare', 'caching', 'headers', 'etag', 'compression',
    'brotli', 'gzip', 'minify', 'hydration', 'layout', 'responsive', 'viewport', 'structureddata',
    'jsonld', 'opengraph', 'twittercard', 'headings', 'anchor', 'internalinks', 'externalinks',
    'hreflang', 'localization', 'geotargeting', 'taxonomies', 'combinatorial', 'matrix', 'facets',
    'aggregations', 'searchintent', 'transactional', 'informational', 'navigational', 'cpc', 'impressions',
    'clickthrough', 'ctr', 'bounce', 'dwelltime', 'snippets', 'featured', 'knowledg盤', 'searchbot',
    'googlebot', 'bingbot', 'yandex', 'duckduckgo', 'xmlchunks', 'sitemapindex', 'lastmod', 'changefreq',
    'prioritytag', 'redirects', 'statuscodes', 'notfound', 'permanentredirect', 'canonicalization',
    'pagination', 'infinite', 'lazyload', 'prefetch', 'preload', 'dnslookup', 'preconnect', 'assetopt',
    'imagecompression', 'webp', 'avif', 'svgopt', 'domnodes', 'renderblocking', 'criticalcss', 'treeshake'
  ],
  'ai-agents': [
    'langgraph', 'langchain', 'crewai', 'autogen', 'swarm', 'orchestrator', 'statemachine', 'agentloop',
    'toolcalling', 'functioncalling', 'jsonschema', 'pydantic', 'guardrails', 'hallucination', 'grounding',
    'embeddings', 'vectorstore', 'vectorsearch', 'faiss', 'pinecone', 'chromadb', 'qdrant', 'milvus',
    'reranker', 'retrieval', 'rag', 'contextwindow', 'tokenlimit', 'chunksize', 'chunkoverlap', 'promptchain',
    'fewshot', 'zeroshot', 'systemprompt', 'chainofthought', 'reactframework', 'reflection', 'selfcritique',
    'evals', 'benchmarks', 'humaninloop', 'approvalgate', 'reviewqueue', 'exceptionhandling', 'fallbackroutine',
    'retrylogic', 'exponentialbackoff', 'concurrency', 'asynctask', 'backgroundworker', 'celery', 'redisqueue',
    'inference', 'latency', 'throughput', 'tokenstreaming', 'sse', 'websockets', 'fine-tuning', 'lora',
    'quantization', 'gguf', 'vllm', 'ollama', 'tgi', 'openai', 'anthropic', 'claude', 'gemini',
    'llama', 'mistral', 'deepseek', 'temperature', 'topp', 'presencepenalty', 'frequencypenalty', 'stopsequences',
    'agentic', 'autonomous', 'triage', 'sentiment', 'intentclassification', 'entityextraction', 'ner',
    'summarization', 'chatmemory', 'bufferhistory', 'sessionstate', 'auditlog', 'telemetry', 'tracing'
  ],
  'web-app-engineering': [
    'nextjs', 'react', 'typescript', 'javascript', 'tailwind', 'shadcn', 'radix', 'framer', 'motion',
    'turbopack', 'webpack', 'babel', 'postcss', 'eslint', 'prettier', 'prettierrc', 'tsconfig', 'modules',
    'servercomponents', 'clientcomponents', 'serveractions', 'apiroutes', 'middleware', 'cookies', 'sessions',
    'authjs', 'nextauth', 'clerk', 'lucia', 'jwt', 'oauth2', 'pkce', 'bearer', 'cors', 'csrf',
    'prisma', 'drizzle', 'supabase', 'postgres', 'postgresql', 'sqlite', 'mongodb', 'mysql', 'redis',
    'migrations', 'seeders', 'indexes', 'foreignkeys', 'transactions', 'pooling', 'pgbouncer', 'queryopt',
    'bundleanalyzer', 'codesplitting', 'dynamicimports', 'treeshaking', 'suspense', 'errorboundary',
    'loadingstate', 'skeleton', 'modals', 'drawers', 'tooltips', 'popovers', 'dropdowns', 'accordions',
    'datatables', 'virtualization', 'tanstack', 'reactquery', 'swr', 'zustand', 'jotai', 'redux',
    'zod', 'superstruct', 'valibot', 'forms', 'reacthookform', 'validation', 'mutation', 'optimisticui',
    'responsivegrid', 'flexbox', 'darkmode', 'lightmode', 'cssvariables', 'webaccessibility', 'aria', 'wcag'
  ],
  'outbound-infrastructure': [
    'dkim', 'spf', 'dmarc', 'mxrecords', 'cname', 'txtrecords', 'dnssec', 'nameservers', 'inboxplacement',
    'deliverability', 'warmup', 'reputation', 'spamtrap', 'blacklist', 'senderid', 'reverseip', 'dedicatedip',
    'iprotation', 'domainrotation', 'mailboxfleet', 'googleworkspace', 'microsoft365', 'outlook', 'smtp',
    'imap', 'pop3', 'mailgun', 'sendgrid', 'postmark', 'resend', 'amazonsee', 'mailchimp', 'instantly',
    'smartlead', 'apollo', 'leadiq', 'zoominfo', 'lusha', 'hunterio', 'dropcontact', 'zerobounce',
    'neverbounce', 'debounce', 'bouncereason', 'softbounce', 'hardbounce', 'spamcomplaint', 'unsubscribe',
    'listcleaning', 'scrubbing', 'mxvalidation', 'smtphandshake', 'greylisting', 'ratelimiting', 'sendlimits',
    'warmupramp', 'peerengagement', 'inboxcalm', 'openrates', 'clickrates', 'replyrates', 'positiveintent',
    'outboundsequence', 'subjectline', 'previewtext', 'spintax', 'dynamicvariables', 'personalizationtokens',
    'secondarydomains', 'domainburn', 'catchall', 'disposableemail', 'corporateinbox', 'salesengagement'
  ],
  'composio-integrations': [
    'composio', 'toolregistry', 'appconnectors', 'oauthflow', 'tokenvault', 'secretmanager', 'authtoken',
    'refreshtoken', 'tokencycle', 'permissionscopes', 'clientid', 'clientsecret', 'redirecturi', 'apigateway',
    'restapi', 'graphql', 'grpc', 'openapi', 'swagger', 'webhooklistener', 'webhooksignature', 'hmac',
    'payloadverification', 'sandboxedexecution', 'dockerbridge', 'isolateruntime', 'resourcelimits',
    'cputhrottling', 'memorycaps', 'executiontimeout', 'failoverqueue', 'retrypolicy', 'deadletterqueue',
    'audittrail', 'telemetrycollector', 'opentelemetry', 'jaeger', 'prometheusmetrics', 'grafanadash',
    'thirdpartyapps', 'githubintegration', 'slackconnector', 'jiraapi', 'linearapp', 'hubspotapi',
    'salesforceapi', 'notionapi', 'googledrive', 'gmailapi', 'clickup', 'airtable', 'stripeapi',
    'intercomapi', 'zendeskapi', 'pipedrive', 'actionbindings', 'tooldefinition', 'parameterschema',
    'functionsignature', 'returnpayload', 'errorhandling', 'statuscodes', 'apiquotas', 'ratebreaker'
  ],
  'cloud-vps-hardening': [
    'ubuntults', 'linuxkernel', 'sysctl', 'firewall', 'ufw', 'iptables', 'fail2ban', 'sshkeys',
    'ed25519', 'sshdconfig', 'rootlogin', 'passwordauth', 'portscan', 'bruteforce', 'intrusionprevention',
    'selinux', 'apparmor', 'systemd', 'journalctl', 'logrotate', 'unattendedupgrades', 'aptupdate',
    'cisbenchmarks', 'dockerdaemon', 'dockersocket', 'rootlessdocker', 'composefile', 'virtualnetwork',
    'bridgenetwork', 'networkisolation', 'containerruntime', 'cgroups', 'namespaces', 'volumemounts',
    'envsecrets', 'dockerhealthcheck', 'restartalways', 'cloudflarezerotrust', 'cloudflared', 'cloudflaretunnel',
    'ingressrules', 'originshield', 'waf', 'ddosdefense', 'ssltermination', 'letsencrypt', 'certbot',
    'tlsconfig', 'tlsciphers', 'hsts', 'corsheaders', 'securityheaders', 'csp', 'xframeoptions',
    'offsitebackup', 'rclone', 's3bucket', 'encryptedbackup', 'gpgencryption', 'disasterrecovery', 'rto',
    'rpo', 'snapshotrestore', 'servermonitoring', 'nodeexporter', 'prometheusalerts', 'alertmanager'
  ],
  'whop-monetization': [
    'whop', 'whopapi', 'whopsdk', 'membershiptiers', 'entitlements', 'accesspasses', 'digitalproducts',
    'licensekeys', 'licensegeneration', 'tokenvalidation', 'checkoutsession', 'checkoutredirect', 'oneclickpay',
    'applepay', 'googlepay', 'stripeconnect', 'paymentintent', 'recurringbilling', 'subscriptioncycle',
    'mrr', 'arr', 'churnrate', 'dunning', 'paymentretry', 'invoicerecovery', 'cancellationflow',
    'downgradeflow', 'proration', 'discordroles', 'discordbot', 'roleassignment', 'rolegating',
    'memberportal', 'customerdashboard', 'affiliateprogram', 'affiliatelink', 'commissiontracking',
    'payouts', 'creatorportal', 'digitaldelivery', 'filehosting', 'softwaregating', 'apigroups',
    'webhookevents', 'membershippurchased', 'membershipcancelled', 'membershipexpired', 'refundissued',
    'disputeevent', 'taxcompliance', 'vatcollection', 'salestax', 'localizedpricing', 'currencyswitch',
    'discountcodes', 'couponrules', 'abandonedcheckout', 'winbackcampaign', 'customerexperience'
  ]
};

const NICHE_KEYWORDS = {
  'b2b-saas': [
    'saas', 'softwareasaserice', 'b2bsaas', 'arr', 'mrr', 'cac', 'ltv', 'paybackperiod',
    'netrevenueentention', 'nrr', 'grossmargin', 'productledgrowth', 'plg', 'salesled', 'enterpriseplan',
    'multitenant', 'singletenant', 'tenantisolation', 'subdomainrouting', 'rolesandpermissions', 'rbac',
    'sso', 'saml', 'okta', 'onelogin', 'directorysync', 'scim', 'audittrails', 'soc2type2', 'isocert',
    'gdpr', 'ccpa', 'securityquestionnaire', 'vendordiligence', 'rfp', 'slacommitment', 'uptimeguarantee',
    'seatpricing', 'usagebased', 'tieredplans', 'featureflags', 'launchdarkly', 'inapponboarding',
    'producttour', 'churnmitigation', 'customerhealthscore', 'gainsight', 'totango', 'hubspotcrm',
    'salesforcecrm', 'pipedrivecrm', 'productqualifiedleads', 'pql', 'marketingqualifiedleads', 'mql',
    'salesqualifiedleads', 'sql', 'demorequest', 'trialconversion', 'productanalytics', 'mixpanel', 'amplitude'
  ],
  'ecommerce-d2c': [
    'ecommerce', 'd2c', 'directtoconsumer', 'shopifyplus', 'woocommerce', 'bigcommerce', 'magento',
    'storefront', 'headlesscommerce', 'skus', 'productcatalog', 'variantinventory', 'stockkeeping',
    'outoffstock', 'backorder', 'preorder', 'productdrops', 'bfcm', 'blackfriday', 'cybermonday',
    'flashsale', 'holidaytraffic', 'promotions', 'discountcode', 'cartabandonment', 'checkoutdropoff',
    'averagordervalue', 'aov', 'repeatpurchaserate', 'customervalue', 'customeracquisition', 'roas',
    'returnonadspend', 'metaads', 'tiktokads', 'googlemerchant', 'productfeed', 'klaviyo', 'emailflows',
    'smscampaigns', 'attentive', 'postscript', 'gorgias', 'zendeskchat', 'ordersupport', 'whereismyorder',
    'wismo', 'returnmerchandise', 'rma', 'loopreturns', 'shippo', 'shipstation', 'thirdpartylogistics',
    '3pl', 'fulfillmentcenter', 'packaging', 'unboxingexperience', 'chargebacks', 'fraudprevention', 'signifyd'
  ],
  'fintech': [
    'fintech', 'financialservices', 'banking', 'neobank', 'bankingasaservice', 'baas', 'corebanking',
    'ledger', 'doubleentry', 'generalledger', 'reconciliation', 'chartofaccounts', 'journalentries',
    'settlement', 'clearinghouse', 'ach', 'nacha', 'fedwire', 'swift', 'sepa', 'fasterpayments',
    'rtp', 'realtimepayments', 'plaid', 'yodlee', 'mxtechnologies', 'stripebanking', 'unitfinance',
    'treasuryprime', 'kyc', 'knowyourcustomer', 'aml', 'antimoneylaundering', 'cdd', 'edd',
    'enhanceddiligence', 'ofac', 'sanctionslist', 'pep', 'politicallyexposed', 'transactionmonitoring',
    'fraudscoring', 'syntheticidentity', 'creditunderwriting', 'loanorigination', 'los', 'debtcovenants',
    'escrow', 'custody', 'brokerdealer', 'finra', 'sec', 'fdic', 'occ', 'pcidss', 'tokenization',
    'cardissuing', 'marqeta', 'lithic', 'paymentgateway', 'interchange', 'merchantaccount', 'payoutrails'
  ],
  'healthtech-biotech': [
    'healthtech', 'digitalhealth', 'biotech', 'telehealth', 'telemedicine', 'clinicaltrials', 'patientcare',
    'hipaa', 'hitech', 'phi', 'protectedhealth', 'businessassociateagreement', 'baa', 'patientportal',
    'intakeforms', 'patientonboarding', 'electronicmedicalrecords', 'emr', 'electronichealthrecords', 'ehr',
    'epic', 'cerner', 'athenahealth', 'allscripts', 'nextgen', 'hl7', 'fhir', 'cda', 'smartonfhir',
    'clinicaldata', 'diagnosticreports', 'labresults', 'teleconsultation', 'providerdirectory', 'credentialing',
    'npi', 'medicallicensing', 'physicianscheduling', 'appointmenttriage', 'symptomchecker', 'prescriptionrouting',
    'e-prescribe', 'surescripts', 'medicalbilling', 'rcm', 'revenuecycle', 'cptcodes', 'icd10', 'claimsprocessing',
    'priorauthorization', 'insuranceroutes', 'medicare', 'medicaid', 'payers', 'pacs', 'dicom', 'medicalimaging'
  ],
  'proptech-realestate': [
    'proptech', 'commercialrealestate', 'cre', 'residentialrealestate', 'brokerage', 'propertyportal',
    'multiplelistingservice', 'mls', 'idx', 'rets', 'reso', 'resowebapi', 'listingfeed', 'syndication',
    'costar', 'loopnet', 'crexi', 'zillow', 'realtorcom', 'yardi', 'realpage', 'appfolio', 'buildium',
    'propertymanagement', 'tenantportal', 'tenantscreening', 'creditcheck', 'evictionhistory', 'leasemanagement',
    'leaseabstraction', 'rentroll', 'proforma', 'netoperatingincome', 'noi', 'capitalizationrate', 'caprate',
    'internalrateofreturn', 'irr', 'cashoncash', 'commercialleases', 'tripleNet', 'nnn', 'tenantimprovements',
    'ti', 'spaceplanning', 'footprint', 'geospatial', 'gismapping', 'neighborhooddata', 'propertytax',
    'parcelid', 'deedrecords', 'realestateinvesting', 'syndicationportal', 'accreditedinvestors', 'equitycrowdfunding'
  ],
  'legaltech-professional': [
    'legaltech', 'lawfirm', 'attorneys', 'lawyers', 'legalpractice', 'corporatelaw', 'litigation',
    'mattermanagement', 'caseintake', 'clientonboarding', 'conflictcheck', 'conflictsofinterest', 'engagementletter',
    'retaineragreement', 'billablehour', 'hourlybilling', 'timekeeping', 'legalbilling', 'clio', 'mycase',
    'smokeball', 'practicepanther', 'imanage', 'netdocuments', 'documentmanagement', 'dms', 'ediscovery',
    'relativity', 'everlaw', 'legalhold', 'redaction', 'contractlifecycle', 'clm', 'ironclad', 'docusign',
    'ndas', 'contractreview', 'depositiontriage', 'courtfiling', 'pacer', 'docketing', 'statuteoflimitations',
    'attorneyclientprivilege', 'workproductdoctrine', 'abamodelrules', 'statebarcompliance', 'legalethics',
    'trustaccounting', 'iolta', 'feecontingency', 'arbitration', 'mediation', 'expertwitness', 'jurisdiction'
  ],
  'venture-capital-private-equity': [
    'venturecapital', 'vc', 'privateequity', 'pe', 'growthcapital', 'buyoutfund', 'assetmanagement',
    'aum', 'generalpartner', 'gp', 'limitedpartner', 'lp', 'capitalcall', 'drypowder', 'waterfall',
    'carriedinterest', 'carry', 'hurdlerate', 'preferredreturn', 'dealsourcing', 'proprietarydealflow',
    'inboundsourcing', 'outboundsourcing', 'thematicinvesting', 'investmentthesis', 'cim', 'confidentialmemo',
    'dataroom', 'virtualdataroom', 'vdr', 'duediligence', 'financialdiligence', 'commercialdiligence',
    'qualityofearnings', 'qofe', 'ebitdamultiples', 'revenuegrowth', 'ruleof40', 'capetable', 'carta',
    'shareholders', 'boardseat', 'portfoliocompanies', 'portco', 'portfolioops', 'operatingpartners',
    'valuecreation', 'synergies', 'add-onacquisitions', 'bolt-on', 'exitstrategy', 'manda', 'secondarysale'
  ],
  'edtech': [
    'edtech', 'onlineeducation', 'digitallearning', 'highered', 'k12', 'universities', 'bootcamps',
    'courseplatform', 'learningmanagementsystem', 'lms', 'canvaslms', 'moodle', 'blackboard', 'brightspace',
    'curriculumbuilder', 'syllabus', 'lecturemodules', 'videohosting', 'vimeoott', 'wistia', 'transcripts',
    'quizzes', 'assessments', 'gradingengine', 'automatedgrading', 'proctoring', 'peerreview', 'certificates',
    'digitalcredentials', 'credly', 'badging', 'accreditation', 'ceu', 'continuingeducation', 'cohortbased',
    'asynchronouslearning', 'synchronouslearning', 'discussionforum', 'communityengagement', 'studentretention',
    'cohortcompletion', 'completionrate', 'drop-offrate', 'learninganalytics', 'scorm', 'xapi', 'tincan',
    'coursemarketplace', 'skillmastery', 'upskilling', 'reskilling', 'corporatelearning', 'enterprisetraining'
  ],
  'cybersecurity': [
    'cybersecurity', 'infosec', 'devsecops', 'networksecurity', 'cloudsecurity', 'ciso', 'securityoperations',
    'soc', 'siem', 'soar', 'splunk', 'datadogsecurity', 'elasticstack', 'sentinel', 'edr', 'xdr',
    'crowdstrike', 'sentinelone', 'endpointdefense', 'firewallrules', 'nextgenfirewall', 'ngfw', 'paloalto',
    'fortinet', 'zerotrust', 'ztna', 'identityaccessmanagement', 'iam', 'privilegedaccess', 'pam',
    'cyberark', 'vulnerabilitymanagement', 'cve', 'cvss', 'zeroday', 'patchmanagement', 'penetrationtesting',
    'redteam', 'blueteam', 'threatintelligence', 'threatactor', 'ransomware', 'malwaredetection', 'phishingdefense',
    'soc2', 'nist', 'cis', 'iso27001', 'hipaasecurity', 'pci-dss', 'encryptionatrest', 'encryptionintransit',
    'tls13', 'sshkeys', 'ed25519', 'bastionhost', 'dmz', 'microsegmentation', 'honeypot', 'intrusiondetection'
  ],
  'agency-consultancy': [
    'agency', 'consultancy', 'consultingfirm', 'growthagency', 'performancemarketing', 'digitalagency',
    'clientretainers', 'monthlyretainer', 'projectfee', 'statementofwork', 'sow', 'scopecreep', 'changeorder',
    'billableutilization', 'realizationrate', 'marginperclient', 'clientonboarding', 'clientportal',
    'whitelabel', 'deliverabletracking', 'campaignreporting', 'lookerstudio', 'clientdashboards', 'highlevel',
    'gohighlevel', 'clickup', 'asana', 'mondaycom', 'clientretention', 'clientchurn', 'accountmanagement',
    'pitchdeck', 'proposals', 'clientprocurement', 'masteragreements', 'msa', 'servicelevelagreement',
    'adspendmanagement', 'mediabuying', 'creativeassets', 'copywritingproduction', 'funnelbuilding',
    'leadgenerationagency', 'seoretainer', 'contentmarketing', 'influencercampaigns', 'agencyvaluation'
  ]
};

// Test pairwise uniqueness of combining SERVICE_KEYWORDS and NICHE_KEYWORDS
const niches = Object.keys(NICHE_KEYWORDS);
const services = Object.keys(SERVICE_KEYWORDS);

const pairs = [];
niches.forEach(n => {
  services.forEach(s => {
    // Word set of this combination
    const words = new Set([...SERVICE_KEYWORDS[s], ...NICHE_KEYWORDS[n]]);
    pairs.push({ slug: `/solutions/${n}/${s}`, words });
  });
});

console.log(`Generated ${pairs.length} combinations.`);

let minDistance = 1.0;
let minPair = '';
let totalTests = 0;

for (let i = 0; i < pairs.length; i++) {
  for (let j = i + 1; j < pairs.length; j++) {
    totalTests++;
    const setA = pairs[i].words;
    const setB = pairs[j].words;
    const intersection = new Set([...setA].filter(x => setB.has(x)));
    const union = new Set([...setA, ...setB]);
    const dist = 1 - (intersection.size / union.size);
    if (dist < minDistance) {
      minDistance = dist;
      minPair = `${pairs[i].slug} vs ${pairs[j].slug}`;
    }
  }
}

console.log(`Total Comparisons: ${totalTests}`);
console.log(`Minimum Uniqueness: ${(minDistance * 100).toFixed(2)}%`);
console.log(`Minimum Pair: ${minPair}`);

module.exports = {
  SERVICE_KEYWORDS,
  NICHE_KEYWORDS
};
