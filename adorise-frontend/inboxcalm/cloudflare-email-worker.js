/**
 * Cloudflare Email Routing Worker for InboxCalm
 * Address: inboxcalm@adorisedigital.com
 * Adorise Digital LLC / Trendy DigiStore LLC
 *
 * This Worker intercepts incoming forwarded hostile emails at Cloudflare edge,
 * forwards them to the InboxCalm NLP/LLM De-escalation Engine,
 * and automatically dispatches an email reply back to the forwarder containing:
 * - Toxicity Rating (0-100) & Threat Classification
 * - 3 Ready-to-copy tactical responses (Diplomatic, Boundary, Executive)
 * - Trial Quota Status & Whop Pro Upgrade Gate
 */

export default {
  async email(message, env, ctx) {
    const fromAddress = message.from;
    const toAddress = message.to;
    const subject = message.headers.get("subject") || "Incoming Email De-escalation";

    console.log(`[InboxCalm Email Worker] Processing email from ${fromAddress} to ${toAddress} with subject "${subject}"`);

    try {
      // 1. Read raw email content from the incoming stream
      const rawEmail = await new Response(message.raw).text();

      // 2. Strip basic MIME headers if raw multipart to get body text
      let bodyText = rawEmail;
      if (rawEmail.includes("\r\n\r\n")) {
        const parts = rawEmail.split("\r\n\r\n");
        // Take content after the initial headers
        bodyText = parts.slice(1).join("\r\n\r\n");
      }

      // Truncate to reasonable token length for safety
      if (bodyText.length > 15000) {
        bodyText = bodyText.substring(0, 15000) + "\n...[truncated]";
      }

      // 3. Post to the InboxCalm Inbound API
      const apiUrl = env.INBOXCALM_API_URL || "https://inboxcalm.adorisedigital.com/api/inbound-email";
      
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Email-Worker-Secret": env.WORKER_SECRET || "inboxcalm-edge-2026"
        },
        body: JSON.stringify({
          from: fromAddress,
          subject: subject,
          body: bodyText
        })
      });

      if (!response.ok) {
        console.error(`[InboxCalm Email Worker] API returned status ${response.status}`);
      } else {
        const result = await response.json();
        console.log(`[InboxCalm Email Worker] Successfully processed. Dispatched: ${result.email_dispatched} via ${result.dispatch_service}`);
      }

      // 4. Optionally forward a copy to the founder's inbox for live monitoring
      const auditForwardEmail = env.FORWARD_AUDIT_EMAIL || "adorisedigital@gmail.com";
      if (auditForwardEmail && auditForwardEmail !== fromAddress) {
        try {
          await message.forward(auditForwardEmail);
        } catch (fwdErr) {
          console.warn("[InboxCalm Email Worker] Audit forward warning:", fwdErr.message);
        }
      }

    } catch (err) {
      console.error("[InboxCalm Email Worker] Unhandled error:", err.message);
    }
  }
};
