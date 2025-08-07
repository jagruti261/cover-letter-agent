
import { motion } from "framer-motion";
import { useState } from "react";
import emailjs from "emailjs-com";

const SERVICE_ID = "service_cty8z1t";
const TEMPLATE_ID = "template_2omer2u";
const PUBLIC_KEY = "TFCmSGoV63bHU-gR9";

export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: ""
  });

  const [status, setStatus] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const validateEmail = (email) => /^\S+@\S+\.\S+$/.test(email);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.name.trim() || !formData.email.trim() || !formData.message.trim()) {
      setStatus({ type: "error", message: "Please fill in all fields." });
      return;
    }

    if (!validateEmail(formData.email)) {
      setStatus({ type: "error", message: "Please enter a valid email address." });
      return;
    }

    setIsSubmitting(true);
    setStatus(null);

    try {
      const result = await emailjs.send(
        SERVICE_ID,
        TEMPLATE_ID,
        {
          name: formData.name,
          email: formData.email,
          message: formData.message
        },
        PUBLIC_KEY
      );

      setStatus({ type: "success", message: "Message sent successfully!" });
      setFormData({ name: "", email: "", message: "" });
    } catch (error) {
      setStatus({ type: "error", message: "Failed to send message. Try again later." });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      className="bg-[#161b22] border border-[#30363d] rounded-lg p-8"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
      viewport={{ once: true }}
      noValidate
    >
      <label className="block mb-6">
        <span className="text-[#7d8590] text-sm mb-1 block">Name</span>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className="w-full rounded-md bg-[#0d1117] border border-[#30363d] px-4 py-3 text-[#f0f6fc] focus:outline-none focus:ring-2 focus:ring-[#7c3aed]"
          placeholder="Your name"
          disabled={isSubmitting}
          required
        />
      </label>

      <label className="block mb-6">
        <span className="text-[#7d8590] text-sm mb-1 block">Email</span>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className="w-full rounded-md bg-[#0d1117] border border-[#30363d] px-4 py-3 text-[#f0f6fc] focus:outline-none focus:ring-2 focus:ring-[#7c3aed]"
          placeholder="you@example.com"
          disabled={isSubmitting}
          required
        />
      </label>

      <label className="block mb-6">
        <span className="text-[#7d8590] text-sm mb-1 block">Message</span>
        <textarea
          name="message"
          value={formData.message}
          onChange={handleChange}
          rows={5}
          className="w-full rounded-md bg-[#0d1117] border border-[#30363d] px-4 py-3 text-[#f0f6fc] focus:outline-none focus:ring-2 focus:ring-[#7c3aed]"
          placeholder="Write your message here..."
          disabled={isSubmitting}
          required
        />
      </label>

      {status && (
        <p
          className={`mb-4 text-sm ${
            status.type === "error" ? "text-[#f85149]" : "text-[#238636]"
          }`}
        >
          {status.message}
        </p>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className={`w-full py-4 rounded-lg font-semibold transition-colors duration-200 ${
          isSubmitting
            ? "bg-[#5850a6] cursor-not-allowed"
            : "bg-[#7c3aed] hover:bg-[#8b5cf6]"
        } text-white`}
      >
        {isSubmitting ? "Sending..." : "Send Message"}
      </button>
    </motion.form>
  );
}
